"""Optional EER execution proof; uses only an isolated in-memory database."""
from pathlib import Path
import sqlite3
HERE=Path(__file__).resolve().parent

def main():
    con=sqlite3.connect(':memory:')
    con.executescript((HERE/'eer-stretcher.sql').read_text())
    out=[]
    def accept(label,sql):
        con.execute(sql);out.append('PASS accepted: '+label)
    def reject(label,sql):
        try:con.execute(sql)
        except sqlite3.IntegrityError as e:out.append('PASS rejected: '+label+' ('+str(e)+')')
        else:raise AssertionError(label+' unexpectedly accepted')
    accept('single CNC',"INSERT INTO machine_single VALUES(1,'cnc',3,NULL)")
    accept('single injection',"INSERT INTO machine_single VALUES(2,'injection',NULL,100)")
    reject('unknown subtype',"INSERT INTO machine_single VALUES(3,'other',NULL,NULL)")
    reject('missing required subtype payload',"INSERT INTO machine_single VALUES(3,'cnc',NULL,NULL)")
    reject('both payloads',"INSERT INTO machine_single VALUES(3,'cnc',3,100)")
    accept('base CNC',"INSERT INTO machine_base VALUES(1,'cnc')")
    accept('CNC child',"INSERT INTO cnc_machine VALUES(1,'cnc',3)")
    reject('overlapping subtype',"INSERT INTO injection_machine VALUES(1,'injection',100)")
    reject('orphan subtype',"INSERT INTO cnc_machine VALUES(999,'cnc',3)")
    accept('base without child demonstrates incomplete coverage',"INSERT INTO machine_base VALUES(2,'injection')")
    rows=con.execute('SELECT b.machine_id FROM machine_base b LEFT JOIN cnc_machine c USING(machine_id) LEFT JOIN injection_machine i USING(machine_id) WHERE c.machine_id IS NULL AND i.machine_id IS NULL').fetchall()
    assert rows==[(2,)]
    out.append('PASS completeness counterexample: base ID 2 has no subtype row')
    text='\n'.join(out)+'\n';(HERE/'eer-results.txt').write_text(text);print(text)
    con.close()
if __name__=='__main__':main()
