# Task 7 — AI-assisted SQL verification

Prepared with ChatGPT and executed on my own computer. Verification results are recorded in [query-results.md](query-results.md).

## Exact prompt used for the query in this package
Here is my SQLite table: readings(ts TEXT, machine TEXT, temp_c REAL, vib_rms REAL, spindle_load REAL). Write a query that returns, for each machine, the average spindle load for readings taken overnight (after 18:00), ordered by average load descending.

## Generated query
```sql
SELECT machine, AVG(spindle_load) AS avg_load
FROM readings
WHERE time(ts) > '18:00:00'
GROUP BY machine
ORDER BY avg_load DESC;
```
In Python, the time is supplied using a `?` bound parameter; see [analyze.py](analyze.py).

## What the query assumes
“After 18:00” is interpreted strictly, excluding exactly 18:00:00. “Overnight” is ambiguous: this query excludes the next morning. If the intended shift is 18:00 inclusive to 06:00 exclusive, use `WHERE time(ts) >= '18:00:00' OR time(ts) < '06:00:00'`. Confirm the intended business rule with the instructor. Grouping nights by their start date would require additional logic.

## Verification
The model produced valid SQLite syntax, grouped each machine separately, and sorted the averages in descending order. The issue is the ambiguous meaning of “overnight”: an evening-only filter does not represent a full night shift. The prepared analysis executes the query, records its EXPLAIN QUERY PLAN, and independently recalculates its result from the CSV with Python. A small boundary dataset checks 18:00:00 and 18:00:01. A deliberately incorrect LIKE '%18%' filter also matches January 18 at noon. This shows why a query that runs successfully can still answer the wrong question.
