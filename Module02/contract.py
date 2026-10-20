"""Corrected contract; execute to emit portable SQLite DDL. No legacy data migration."""
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, Table, MetaData, CheckConstraint, create_engine, event
from sqlalchemy.schema import CreateTable

PositiveID = Annotated[int, Field(strict=True, ge=1)]
Text = Annotated[str, Field(min_length=1)]
class InputModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
class Machine(InputModel):
    machine_id: PositiveID
    serial_no: str = Field(pattern=r'^SN-.+$')
    site: Text
    installed: date
class Part(InputModel):
    part_no: str = Field(pattern=r'^P-.+$')
    description: Text
    unit_price: Decimal = Field(ge=0, max_digits=9, decimal_places=2, allow_inf_nan=False)
class Technician(InputModel):
    technician_id: PositiveID
    name: Text
class MaintenanceJob(InputModel):
    job_id: PositiveID
    machine_id: PositiveID
    technician_id: PositiveID
    done_on: date
    part_nos: list[Annotated[str, Field(pattern=r'^P-.+$')]] = Field(default_factory=list)
    @field_validator('part_nos')
    @classmethod
    def no_duplicates(cls, values):
        if len(set(values)) != len(values):
            raise ValueError('a part can occur only once per job')
        return values
metadata = MetaData()
def date_check(c):
    # Calendar validity remains an application rule; DB checks ISO shape only.
    return CheckConstraint(f"length({c})=10 AND {c} GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'",name=f'ck_{c}_shape')
machine_t=Table('machine',metadata,
 Column('machine_id',Integer,primary_key=True),Column('serial_no',String,nullable=False,unique=True),
 Column('site',String,nullable=False),Column('installed',Date,nullable=False),
 CheckConstraint('machine_id>0'),CheckConstraint("serial_no LIKE 'SN-%' AND length(serial_no)>3"),
 CheckConstraint('length(trim(site))>0'),date_check('installed'))
part_t=Table('part',metadata,Column('part_no',String,primary_key=True,nullable=False),
 Column('description',String,nullable=False),Column('unit_price',Numeric(9,2),nullable=False),
 CheckConstraint("part_no LIKE 'P-%' AND length(part_no)>2"),CheckConstraint('length(trim(description))>0'),
 CheckConstraint("typeof(unit_price) IN ('integer','real') AND unit_price>=0 AND unit_price<=9999999.99 AND abs(unit_price*100-round(unit_price*100))<0.000001",name='ck_money'))
technician_t=Table('technician',metadata,Column('technician_id',Integer,primary_key=True),Column('name',String,nullable=False),CheckConstraint('technician_id>0'),CheckConstraint('length(trim(name))>0'))
maint_job_t=Table('maint_job',metadata,Column('job_id',Integer,primary_key=True),
 Column('machine_id',Integer,ForeignKey('machine.machine_id'),nullable=False),
 Column('technician_id',Integer,ForeignKey('technician.technician_id'),nullable=False),
 Column('done_on',Date,nullable=False),CheckConstraint('job_id>0'),date_check('done_on'))
job_part_t=Table('job_part',metadata,
 Column('job_id',Integer,ForeignKey('maint_job.job_id'),primary_key=True,nullable=False),
 Column('part_no',String,ForeignKey('part.part_no'),primary_key=True,nullable=False))
def make_engine(url='sqlite://'):
    engine=create_engine(url)
    @event.listens_for(engine,'connect')
    def foreign_keys(dbapi_connection, record):
        cursor=dbapi_connection.cursor();cursor.execute('PRAGMA foreign_keys=ON');cursor.close()
    return engine
def ddl():
    engine=make_engine()
    return 'PRAGMA foreign_keys=ON;\n\n'+'\n\n'.join(str(CreateTable(t).compile(engine)).strip()+';' for t in metadata.sorted_tables)+'\n'
if __name__=='__main__':
    result=ddl();Path(__file__).with_name('corrected-schema.sql').write_text(result,encoding='utf-8');print(result)
