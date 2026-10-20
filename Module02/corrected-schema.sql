PRAGMA foreign_keys=ON;

CREATE TABLE machine (
	machine_id INTEGER NOT NULL, 
	serial_no VARCHAR NOT NULL, 
	site VARCHAR NOT NULL, 
	installed DATE NOT NULL, 
	PRIMARY KEY (machine_id), 
	CHECK (machine_id>0), 
	CHECK (serial_no LIKE 'SN-%' AND length(serial_no)>3), 
	CHECK (length(trim(site))>0), 
	CONSTRAINT ck_installed_shape CHECK (length(installed)=10 AND installed GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'), 
	UNIQUE (serial_no)
);

CREATE TABLE part (
	part_no VARCHAR NOT NULL, 
	description VARCHAR NOT NULL, 
	unit_price NUMERIC(9, 2) NOT NULL, 
	PRIMARY KEY (part_no), 
	CHECK (part_no LIKE 'P-%' AND length(part_no)>2), 
	CHECK (length(trim(description))>0), 
	CONSTRAINT ck_money CHECK (typeof(unit_price) IN ('integer','real') AND unit_price>=0 AND unit_price<=9999999.99 AND abs(unit_price*100-round(unit_price*100))<0.000001)
);

CREATE TABLE technician (
	technician_id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (technician_id), 
	CHECK (technician_id>0), 
	CHECK (length(trim(name))>0)
);

CREATE TABLE maint_job (
	job_id INTEGER NOT NULL, 
	machine_id INTEGER NOT NULL, 
	technician_id INTEGER NOT NULL, 
	done_on DATE NOT NULL, 
	PRIMARY KEY (job_id), 
	CHECK (job_id>0), 
	CONSTRAINT ck_done_on_shape CHECK (length(done_on)=10 AND done_on GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'), 
	FOREIGN KEY(machine_id) REFERENCES machine (machine_id), 
	FOREIGN KEY(technician_id) REFERENCES technician (technician_id)
);

CREATE TABLE job_part (
	job_id INTEGER NOT NULL, 
	part_no VARCHAR NOT NULL, 
	PRIMARY KEY (job_id, part_no), 
	FOREIGN KEY(job_id) REFERENCES maint_job (job_id), 
	FOREIGN KEY(part_no) REFERENCES part (part_no)
);
