"""Windows-compatible reproducible evidence runner; only Module02 outputs are written."""
from pathlib import Path
import sqlite3,sys,platform,io,unittest
import pydantic,sqlalchemy
from contract import ddl
HERE=Path(__file__).resolve().parent

def execute_script(con, source):
    output=[];statement=''
    for line in source.splitlines():
        statement+=line+'\n'
        if sqlite3.complete_statement(statement):
            cur=con.execute(statement)
            output.append(statement.strip())
            if cur.description:
                output.append(' | '.join(x[0] for x in cur.description))
                output.extend(' | '.join('NULL' if x is None else str(x) for x in row) for row in cur.fetchall())
            statement=''
    if statement.strip(): raise ValueError('incomplete SQL')
    return '\n'.join(output)+'\n'
def main():
    with sqlite3.connect(HERE/'legacy.db') as con:
        con.executescript((HERE/'legacy_setup.sql').read_text(encoding='utf-8'))
        assert [con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0] for t in ['machine','part','maint_job']]==[4,4,4]
        for name in ['cardinality','integrity']:
            result=execute_script(con,(HERE/f'{name}-audit.sql').read_text())
            (HERE/f'{name}-results.txt').write_text(result,encoding='utf-8')
        # Assert the observed defects, not merely that each SELECT executes.
        assert con.execute("SELECT j.job_id,j.machine_name FROM maint_job j LEFT JOIN machine m USING(machine_name) WHERE m.machine_name IS NULL").fetchall()==[(3,'cnc-05')]
        assert con.execute("SELECT part_no,COUNT(*) FROM part GROUP BY part_no HAVING COUNT(*)>1").fetchall()==[('P-1003',2)]
        assert con.execute("SELECT part_no FROM part WHERE unit_price<'15'").fetchall()==[('P-1001',)]
        assert con.execute("SELECT part_no FROM part WHERE CAST(unit_price AS NUMERIC)<15 ORDER BY part_no").fetchall()==[('P-1001',),('P-1003',),('P-1003',)]
        assert con.execute("SELECT machine_name FROM machine WHERE installed='unknown'").fetchall()==[('RANDOM-NAME',)]
        assert con.execute("SELECT j.job_id FROM maint_job j JOIN part p ON p.part_no=j.parts_used ORDER BY j.job_id").fetchall()==[(2,),(2,),(3,)]
    with sqlite3.connect(':memory:') as con:
        out=execute_script(con,(HERE/'sketch-proof.sql').read_text())
        try: con.execute("INSERT INTO sensor VALUES(12,999,'temperature')")
        except sqlite3.IntegrityError as e: out+='EXPECTED rejection: '+str(e)+'\n'
        else: raise AssertionError('orphan accepted')
        (HERE/'sketch-proof-results.txt').write_text(out)
    (HERE/'corrected-schema.sql').write_text(ddl())
    with sqlite3.connect(':memory:') as con:
        con.executescript(ddl());assert len(con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())==5
    env=f'Python {platform.python_version()}\nSQLite {sqlite3.sqlite_version}\nPydantic {pydantic.__version__}\nSQLAlchemy {sqlalchemy.__version__}\nPlatform {platform.platform()}\n'
    (HERE/'environment.txt').write_text(env)
    suite=unittest.defaultTestLoader.discover(str(HERE/'tests'))
    buf=io.StringIO();result=unittest.TextTestRunner(stream=buf,verbosity=2).run(suite)
    (HERE/'test-results.txt').write_text(buf.getvalue());print(env+buf.getvalue())
    if not result.wasSuccessful():sys.exit(1)
    print('PASS: fixture, audits, sketch proof, DDL reconstruction and contract tests')
if __name__=='__main__':main()
