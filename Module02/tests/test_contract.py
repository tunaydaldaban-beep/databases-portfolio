import sys,sqlite3,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pydantic import ValidationError
from contract import Machine,Part,MaintenanceJob,Technician,ddl,metadata,make_engine
class ModelTests(unittest.TestCase):
    def machine(self,**kw):
        v=dict(machine_id=1,serial_no='SN-1',site='Gutersloh',installed='2020-02-29');v.update(kw);return Machine(**v)
    def test_valid(self):self.assertEqual(self.machine().installed.year,2020)
    def test_serial(self):
        with self.assertRaises(ValidationError):self.machine(serial_no='BAD')
    def test_calendar_date(self):
        with self.assertRaises(ValidationError):self.machine(installed='2021-02-29')
    def test_missing(self):
        with self.assertRaises(ValidationError):Machine(machine_id=1)
    def test_positive_id(self):
        with self.assertRaises(ValidationError):self.machine(machine_id=0)
    def test_blank_site(self):
        with self.assertRaises(ValidationError):self.machine(site=' ')
    def test_valid_part(self):self.assertEqual(str(Part(part_no='P-1',description='Bearing',unit_price='12.50').unit_price),'12.50')
    def test_bad_prices(self):
        for price in ['-1','abc','NaN','1.001','10000000']:
            with self.subTest(price=price),self.assertRaises(ValidationError):Part(part_no='P-1',description='x',unit_price=price)
    def test_duplicate_parts(self):
        with self.assertRaises(ValidationError):MaintenanceJob(job_id=1,machine_id=1,technician_id=1,done_on='2026-01-01',part_nos=['P-1','P-1'])
    def test_valid_job(self):self.assertEqual(MaintenanceJob(job_id=1,machine_id=1,technician_id=1,done_on='2026-01-01').part_nos,[])
    def test_valid_technician(self):self.assertEqual(Technician(technician_id=1,name='Beier').name,'Beier')
class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.c=sqlite3.connect(':memory:');self.c.executescript(ddl())
        self.c.executescript("INSERT INTO machine VALUES(1,'SN-1','Gutersloh','2020-01-01');INSERT INTO technician VALUES(1,'Beier');INSERT INTO part VALUES('P-1','Bearing',12.50);INSERT INTO maint_job VALUES(1,1,1,'2026-01-01');INSERT INTO job_part VALUES(1,'P-1');")
    def tearDown(self):self.c.close()
    def reject(self,s):
        with self.assertRaises(sqlite3.IntegrityError):self.c.execute(s)
    def test_fk_enabled(self):self.assertEqual(self.c.execute('PRAGMA foreign_keys').fetchone()[0],1)
    def test_duplicate_serial(self):self.reject("INSERT INTO machine VALUES(2,'SN-1','x','2020-01-01')")
    def test_orphan_machine(self):self.reject("INSERT INTO maint_job VALUES(2,999,1,'2026-01-01')")
    def test_orphan_technician(self):self.reject("INSERT INTO maint_job VALUES(2,1,999,'2026-01-01')")
    def test_duplicate_pair(self):self.reject("INSERT INTO job_part VALUES(1,'P-1')")
    def test_orphan_part(self):self.reject("INSERT INTO job_part VALUES(1,'P-404')")
    def test_duplicate_part(self):self.reject("INSERT INTO part VALUES('P-1','x',1)")
    def test_negative_price(self):self.reject("INSERT INTO part VALUES('P-2','x',-1)")
    def test_text_price(self):self.reject("INSERT INTO part VALUES('P-2','x','free')")
    def test_fractional_cent(self):self.reject("INSERT INTO part VALUES('P-2','x',1.001)")
    def test_null_required(self):self.reject("INSERT INTO machine VALUES(2,'SN-2',NULL,'2020-01-01')")
    def test_many_to_many(self):
        self.c.executescript("INSERT INTO part VALUES('P-2','belt',48);INSERT INTO maint_job VALUES(2,1,1,'2026-01-02');INSERT INTO job_part VALUES(1,'P-2'),(2,'P-1');")
        self.assertEqual(self.c.execute('SELECT job_id,COUNT(*) FROM job_part GROUP BY job_id').fetchall(),[(1,2),(2,1)])
    def test_parent_delete(self):self.reject('DELETE FROM machine WHERE machine_id=1')
    def test_sqlalchemy_fk(self):
        e=make_engine();metadata.create_all(e)
        with e.connect() as c:self.assertEqual(c.exec_driver_sql('PRAGMA foreign_keys').scalar(),1)
        e.dispose()
if __name__=='__main__':unittest.main()
