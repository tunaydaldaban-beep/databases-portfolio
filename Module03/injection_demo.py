"""Local teaching fixture only: compare unsafe SQL construction and binding."""
import sqlite3
from pathlib import Path

def vulnerable(conn, name):
    return conn.execute(f"SELECT customer_id, name FROM customer WHERE name = '{name}'").fetchall()

def safe(conn, name):
    return conn.execute('SELECT customer_id, name FROM customer WHERE name = ?', (name,)).fetchall()

def demo():
    db = Path(__file__).with_name('warehouse.db')
    if not db.exists():
        raise SystemExit('Run python Module03/bench.py first.')
    conn = sqlite3.connect(db)
    lines = []
    try:
        lines.append(f'normal: {vulnerable(conn, "Customer 1")}')
        try:
            vulnerable(conn, "O'Brien")
            raise AssertionError('Expected apostrophe syntax error')
        except sqlite3.OperationalError as exc:
            lines.append(f'apostrophe crash: {exc}')
        payload = "' OR '1'='1"
        injected = vulnerable(conn, payload)
        assert len(injected) == 2000
        assert safe(conn, payload) == []
        lines.extend([f'payload: {payload}', f'unsafe payload: {len(injected)} rows', f'safe payload: {safe(conn, payload)}'])
        conn.execute('INSERT INTO customer VALUES (?, ?, ?)', (2001, "O'Brien", 'Test'))
        assert safe(conn, "O'Brien") == [(2001, "O'Brien")]
        lines.append(f'safe apostrophe: {safe(conn, "O\'Brien")}')
    finally:
        conn.rollback()  # Temporary name fixture never persists.
        conn.close()
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    output = demo()
    Path(__file__).with_name('injection-output.txt').write_text(output, encoding='utf-8')
    print(output)
