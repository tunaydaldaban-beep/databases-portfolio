-- Orphan job
SELECT m.job_id, m.machine_name FROM maint_job m LEFT JOIN machine x ON m.machine_name=x.machine_name WHERE x.machine_name IS NULL;
-- Duplicate part
SELECT part_no, COUNT(*) AS copies FROM part GROUP BY part_no HAVING COUNT(*)>1;
-- Incorrect lexical comparison
SELECT part_no,unit_price FROM part WHERE unit_price < '15';
-- Numeric comparison for this known fixture (not a general input validator)
SELECT part_no,unit_price FROM part WHERE CAST(unit_price AS NUMERIC)<15;
-- Date shape
SELECT machine_name,installed FROM machine WHERE installed NOT GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]';
-- Incorrect join loses multi-part jobs and duplicates job 2
SELECT j.job_id,p.description FROM maint_job j JOIN part p ON p.part_no=j.parts_used;
