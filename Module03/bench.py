"""Rebuild only Module03/warehouse.db; record real plans, timings and checks."""
import json
import platform
import sqlite3
import statistics
import time
from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).resolve().parent
INDEXES = {
    'date': 'CREATE INDEX ix_orders_ordered_on ON orders(ordered_on)',
    'order': 'CREATE INDEX ix_orderline_order ON order_line(order_id)',
    'product': 'CREATE INDEX ix_orderline_product ON order_line(product_id)',
}
DAY = "SELECT o.order_id, o.ordered_on, c.name FROM orders o JOIN customer c ON c.customer_id=o.customer_id WHERE o.ordered_on='2026-02-14'"
GROUPED = "SELECT c.customer_id,c.name,COUNT(*) AS late_orders FROM orders o JOIN customer c ON c.customer_id=o.customer_id WHERE o.status='late' GROUP BY c.customer_id,c.name ORDER BY late_orders DESC,c.customer_id"
CORRELATED = "SELECT c.customer_id,c.name,(SELECT COUNT(*) FROM orders o WHERE o.customer_id=c.customer_id AND o.status='late') AS late_orders FROM customer c WHERE EXISTS(SELECT 1 FROM orders o WHERE o.customer_id=c.customer_id AND o.status='late') ORDER BY late_orders DESC,c.customer_id"
WINDOW = "SELECT DISTINCT c.customer_id,c.name,COUNT(*) OVER(PARTITION BY c.customer_id) AS late_orders FROM orders o JOIN customer c ON c.customer_id=o.customer_id WHERE o.status='late' ORDER BY late_orders DESC,c.customer_id"

def plan(conn, sql):
    return [r[3] for r in conn.execute('EXPLAIN QUERY PLAN '+sql)]

def measure(conn, sql, batch):
    conn.execute(sql).fetchall()  # Same warm-up for every cell.
    samples = []
    for _ in range(3):
        start = time.perf_counter()
        for _ in range(batch):
            conn.execute(sql).fetchall()
        samples.append((time.perf_counter()-start)*1000/batch)
    return {'samples_ms': samples, 'median_ms': statistics.median(samples), 'batch': batch}

def main():
    conn = sqlite3.connect(HERE/'warehouse.db', cached_statements=0)
    conn.executescript((HERE/'setup.sql').read_text(encoding='utf-8'))
    counts = {t:conn.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in ['customer','product','orders','order_line']}
    assert counts == {'customer':2000,'product':500,'orders':60000,'order_line':240000}
    sql = (HERE/'queries.sql').read_text(encoding='utf-8')
    queries = {'dashboard':sql,'single_day':DAY,'wrapped_date':DAY.replace("o.ordered_on='", "date(o.ordered_on)='"), 'product_filter':'SELECT SUM(qty) FROM order_line WHERE product_id=42'}
    expected = {name:conn.execute(q).fetchall() for name,q in queries.items()}
    records = []
    stages = [('baseline',[]),('date only',['date']),('order only',['order']),('product only',['product']),('date + order',['date','order']),('all three',['date','order','product'])]
    for stage, keys in stages:
        for ddl in INDEXES.values():
            conn.execute('DROP INDEX IF EXISTS '+ddl.split()[2])
        for key in keys:
            conn.execute(INDEXES[key])
        conn.commit()
        for name,q in queries.items():
            actual_plan = plan(conn,q)  # Capture before measuring.
            assert conn.execute(q).fetchall() == expected[name]
            record = {'stage':stage,'query':name,'plan':actual_plan,**measure(conn,q,1 if name=='dashboard' else 30)}
            records.append(record)
    # Independent procedural recomputation of the dashboard from base tables.
    customers = {i:city for i,city in conn.execute('SELECT customer_id,city FROM customer')}
    prices = dict(conn.execute('SELECT product_id,price FROM product'))
    orders = {i:(cid,date) for i,cid,date in conn.execute('SELECT order_id,customer_id,ordered_on FROM orders')}
    revenue = defaultdict(float); seen = defaultdict(set)
    for oid,pid,qty in conn.execute('SELECT order_id,product_id,qty FROM order_line'):
        cid,date = orders[oid]
        if '2025-01-01' <= date < '2026-01-01':
            city = customers[cid]; revenue[city] += qty*prices[pid]; seen[city].add(cid)
    assert sorted(expected['dashboard']) == sorted((city,len(seen[city]),amount) for city,amount in revenue.items())
    # Small fixture covers repeated customer/lines and exact date boundaries.
    fixture = sqlite3.connect(':memory:')
    schema = (HERE/'setup.sql').read_text(encoding='utf-8').split('-- 2,000 customers')[0]
    fixture.executescript(schema)
    fixture.executemany('INSERT INTO customer VALUES(?,?,?)',[(1,'A','X'),(2,'B','X'),(3,'No orders','Y')])
    fixture.execute("INSERT INTO product VALUES(1,'SKU',10)")
    fixture.executemany('INSERT INTO orders VALUES(?,?,?,?)',[(1,1,'2025-01-01','late'),(2,1,'2025-12-31','open'),(3,2,'2026-01-01','late'),(4,2,'2024-12-31','late'),(5,2,'2025-06-01','open')])
    fixture.executemany('INSERT INTO order_line VALUES(?,?,?)',[(1,1,2),(1,1,3),(2,1,1),(3,1,100),(4,1,100)])
    assert fixture.execute(sql).fetchall() == [('X',1,60.0)]
    fixture.close()
    # Stretcher: same semantics (only customers with late orders), stable tie order.
    stretch = []
    reference = conn.execute(GROUPED).fetchall()
    for name,q in [('grouped',GROUPED),('correlated',CORRELATED),('window',WINDOW)]:
        p = plan(conn,q)
        result = conn.execute(q).fetchall()
        assert result == reference
        stretch.append({'name':name,'sql':q,'plan':p,'rows':len(result),'first_rows':result[:3]})
    # Safari uses a disposable copy; Module02 files/database are untouched.
    legacy = sqlite3.connect(':memory:', cached_statements=0)
    legacy.executescript((HERE.parent/'Module02/legacy_setup.sql').read_text(encoding='utf-8'))
    safari = []
    safari_queries = ["SELECT * FROM maint_job WHERE technician='Beier'", "SELECT * FROM machine WHERE machine_name='cnc-02'", "SELECT * FROM maint_job WHERE technician LIKE '%ei%'", "SELECT * FROM maint_job WHERE lower(technician)='beier'"]
    for stage in ['before','after']:
        if stage=='after': legacy.execute('CREATE INDEX ix_job_tech ON maint_job(technician)')
        for q in safari_queries: safari.append({'stage':stage,'sql':q,'plan':plan(legacy,q)})
    legacy.executescript('CREATE TABLE t(a INTEGER,b TEXT); CREATE INDEX i ON t(a);')
    covering = {q:plan(legacy,q) for q in ['SELECT a FROM t WHERE a=1','SELECT a,b FROM t WHERE a=1']}
    try:
        conn.execute('SELECT city,COUNT(*) AS n FROM customer WHERE COUNT(*)>1 GROUP BY city').fetchall()
        raise AssertionError('Expected aggregate misuse')
    except sqlite3.OperationalError as exc: clause_error=str(exc)
    assert len(conn.execute('SELECT city,COUNT(*) AS n FROM customer GROUP BY city HAVING COUNT(*)>1').fetchall()) == 4
    output = {'environment':{'python':platform.python_version(),'sqlite':sqlite3.sqlite_version,'platform':platform.platform(),'execution':'Executed locally on Tunay Windows computer','timing':'One connection, no ANALYZE, cached_statements=0, one warm-up then 3 samples, fully fetched rows; short queries batched 30 times'},'counts':counts,'dashboard':expected['dashboard'],'records':records,'safari':safari,'covering':covering,'stretcher':stretch,'checks':['Row counts','Results unchanged across all index stages','Independent Python dashboard calculation','Boundary fixture: start/end dates, duplicate lines, customer without orders, order without lines','All three late-order rewrites agree','Aggregate WHERE fails; HAVING succeeds'],'clause_error':clause_error}
    (HERE/'results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Measured query plans and benchmark','',f"Python {platform.python_version()}; SQLite {sqlite3.sqlite_version}. Executed locally on Tunay's Windows computer.",'','Run `python Module03/bench.py` from the repository root to regenerate. Rebuilds only Module03/warehouse.db. All times are milliseconds per fully fetched query; warm-up plus median of 3 samples; 30-query batches for short queries. Same connection, no ANALYZE. Timings include Python overhead and warm caches. See [raw samples](results.json).','','| Stage | Dashboard ms | Single-day ms | Wrapped date ms | Product filter ms |','|---|---:|---:|---:|---:|']
    for stage,_ in stages:
        row=[r for r in records if r['stage']==stage]
        lines.append('| '+stage+' | '+' | '.join(f"{r['median_ms']:.3f}" for r in row)+' |')
    lines += ['','## Dashboard result','','| City | Distinct customers | Revenue |','|---|---:|---:|']
    lines += [f'| {city} | {n} | {amount:.2f} |' for city,n,amount in expected['dashboard']]
    lines += ['','## Exact plans']
    for r in records:
        lines += ['',f"### {r['stage']} / {r['query']}",'','```text',*r['plan'],'```']
    lines += ['','## Verification','',*['- PASS: '+x for x in output['checks']],'','Fixture expected result: X / 1 customer / 60.00 revenue. The order without lines is excluded by INNER JOIN; a city without qualifying lines is absent.','',f'Invalid aggregate WHERE error: `{clause_error}`.']
    (HERE/'benchmark.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    extra=['# Plan safari, covering indexes and rewrites','','Predictions were recorded in [predictions.md](predictions.md) before execution.']
    for r in safari: extra += ['',f"## Safari {r['stage']}",'','```sql',r['sql']+';','```','```text',*r['plan'],'```']
    for q,p in covering.items(): extra += ['','## Covering demo','','```sql',q+';','```','```text',*p,'```']
    for r in stretch: extra += ['',f"## {r['name']} rewrite",'', '```sql',r['sql']+';','```','```text',*r['plan'],'```',f"Rows: {r['rows']}; first rows: {r['first_rows']}"]
    extra += ['','All rewrites return the same rows, excluding customers with zero late orders. The grouped query is the default AI-assisted choice and simplest to read. The correlated version repeats work per customer and has no customer_id index here. The window version preserves rows before DISTINCT removes duplicates. Secondary customer_id ordering makes tied counts deterministic.']
    (HERE/'extra-plans.md').write_text('\n'.join(extra)+'\n',encoding='utf-8')
    conn.close(); legacy.close()
    print(json.dumps({'counts':counts,'dashboard':expected['dashboard'],'checks':output['checks']},indent=2))

if __name__=='__main__': main()
