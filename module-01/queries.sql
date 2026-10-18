SELECT machine, COUNT(*) AS n FROM readings GROUP BY machine;
SELECT machine, MAX(vib_rms) AS peak_vib FROM readings GROUP BY machine;
SELECT COUNT(*) AS alarms FROM readings WHERE vib_rms > 2.0;
SELECT machine, AVG(spindle_load) AS avg_load
FROM readings
WHERE time(ts) > '18:00:00'
GROUP BY machine
ORDER BY avg_load DESC;
