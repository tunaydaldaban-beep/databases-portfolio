# Module 03 — LLM-Assisted SQL & Query Profiling

[← Portfolio](../README.md) · [Feedback walkthrough](../FEEDBACK-GUIDE.md)

## Status

The technical tasks were completed and verified locally on my Windows computer. Reflection 03 is complete.

My relational-algebra practice is recorded, including guided examples, my own attempt on a new condition, and feedback correcting the numeric literal.

I discussed the module with İsa. A detailed peer comparison of SQLite versions and query plans is still pending.

## Start here: one claim, one proof

> An index can make a selective query much faster, but can make a broad aggregate query slower. The query plan helps explain what changed.

Open [benchmark.md](benchmark.md):

1. Compare baseline versus date-only for the single-day lookup. The plan changes from SCAN to SEARCH, and the recorded execution time decreases.
2. Compare baseline versus date + order for the annual dashboard. The plan changes, but the recorded execution time increases.

These results show why index decisions should be checked against both query plans and actual measurements.

## Tasks and evidence

| Learning goal / task | Evidence |
|---|---|
| Data setup and repeatable execution | [setup.sql](setup.sql), [bench.py](bench.py) |
| AI-assisted joins, aggregates and correctness checks | [queries.sql](queries.sql), [sql-notes.md](sql-notes.md) |
| AI-provided predictions before initial execution | [predictions.md](predictions.md) |
| Index comparison, negative result and timing | [benchmark.md](benchmark.md), [raw samples](results.json) |
| Apostrophe crash, injection payload and safe parameters | [injection_demo.py](injection_demo.py), [output](injection-output.txt) |
| Relational-algebra practice, original answer and correction | [sql-notes.md](sql-notes.md#relational-algebra-and-sql) |
| SQL clause order and setup curiosities | [sql-notes.md](sql-notes.md) |
| Plan safari, covering index and optional query rewrites | [extra-plans.md](extra-plans.md) |
| Personal learning reflection | [ref03.md](../Reflections/ref03.md) |

The predictions in predictions.md were supplied by AI. They are not presented as independent student predictions.

## Run from the repository root

In PowerShell or a terminal:

```powershell
python Module03/bench.py
python Module03/injection_demo.py
```

Only Python's standard library is needed.

The Python and SQLite versions used for the recorded benchmark are listed in [results.json](results.json). The course recommends Python 3.14.

The benchmark rebuilds **Module03/warehouse.db** and overwrites generated benchmark evidence files. Save any personal changes to the generated database before rerunning.

For the plan safari, the script uses an in-memory copy of Module02's setup. It does not change Module02/legacy.db.

### Optional sqlite3 CLI setup

These commands also work in PowerShell:

```powershell
sqlite3 Module03/warehouse.db ".read Module03/setup.sql"
sqlite3 Module03/warehouse.db ".read Module03/queries.sql"
```

Running setup resets the indexes. Run bench.py for the full index comparison.

A local rerun may produce different timings or plans. Keep the actual results and explain what they show.

## Verification summary

The benchmark checks:

- Expected row counts: 2,000 customers, 500 products, 60,000 orders and 240,000 order lines.
- Unchanged query results across index configurations.
- Dashboard results against a separate Python calculation.
- Date boundaries, repeated lines and customers, customers without orders, and orders without lines.
- Agreement between grouped, correlated-subquery and window-function reports.
- An aggregate condition failing in WHERE and succeeding in HAVING.

The injection demonstration checks:

- A normal customer lookup.
- An apostrophe causing an error in the unsafe query.
- An injection payload returning all customers in the unsafe query.
- Bound parameters treating the payload as data.
- A name containing an apostrophe working correctly with bound parameters.

## Relational-algebra practice

After guided practice with technician-name filters, I attempted:

```sql
SELECT *
FROM maint_job
WHERE job_id = 5;
```

My initial answer was:

```text
sigma job_id = '5' (maint_job)
```

I selected the correct operator, column and table. After feedback, I removed the quotes around the numeric value:

```text
σ job_id = 5 (maint_job)
```

The full practice record and explanation are in [SQL notes](sql-notes.md#relational-algebra-and-sql).

## Peer discussion and remaining activities

I discussed the module with İsa. We both found organizing the work and finding small mistakes challenging.

This was a general discussion. The following activities are still pending:

- A detailed comparison of SQLite versions and query plans with another pod.
- Curiosity swaps and recorded feedback.

No question posted to #sql-questions is documented yet.

## Presentation route

1. Open [queries.sql](queries.sql) and explain the joins, date filter and aggregates.
2. Open [benchmark.md](benchmark.md) and compare the selective lookup with the annual dashboard.
3. Open [injection_demo.py](injection_demo.py) and explain the bound-parameter line.
4. Open [SQL notes](sql-notes.md#relational-algebra-and-sql) and explain the selection example.
5. Finish with [Reflection 03](../Reflections/ref03.md): what I learned, what was difficult and how this relates to practical database work.