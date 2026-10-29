# Module 03 — LLM-Assisted SQL & Query Profiling

[← Portfolio](../README.md)

## Status

Technical tasks were completed and verified locally on my Windows computer. [Reflection 03](../Reflections/ref03.md) is complete.

I discussed the module with İsa. A detailed peer comparison of query plans and an independent relational-algebra attempt are still pending.

## Main finding

An index can make a selective query much faster, but can make a broad aggregate query slower. The query plan shows which access path SQLite used.

In [benchmark.md](benchmark.md), compare:

- **baseline → date only:** the single-day query changes from SCAN to SEARCH using the date index and runs faster.
- **baseline → date + order:** the annual dashboard uses indexed lookups but takes longer in the recorded measurements.
- **date only / wrapped_date:** wrapping the date column in a function prevents a search using the ordinary date index.

## Evidence

| Learning goal / task | Evidence |
|---|---|
| Dataset setup and reproducible execution | [setup.sql](setup.sql), [bench.py](bench.py) |
| AI-assisted SQL and correctness verification | [queries.sql](queries.sql), [sql-notes.md](sql-notes.md) |
| AI-provided predictions before execution | [predictions.md](predictions.md) |
| Index benchmarks and negative results | [benchmark.md](benchmark.md), [raw samples](results.json) |
| SQL injection and bound parameters | [injection_demo.py](injection_demo.py), [output](injection-output.txt) |
| Relational algebra, clause order and study notes | [sql-notes.md](sql-notes.md) |
| Plan safari, covering indexes and optional query rewrites | [extra-plans.md](extra-plans.md) |
| Personal reflection | [ref03.md](../Reflections/ref03.md) |

## Local verification

I ran both Python scripts on my Windows computer. The benchmark checks passed:

- Expected table row counts.
- Unchanged query results across index configurations.
- Dashboard results matching a separate Python calculation.
- Date boundaries, repeated order lines and customers without qualifying lines.
- Matching results from the grouped, correlated-subquery and window-function versions.
- An invalid aggregate in WHERE failing, while the HAVING version succeeds.

The injection demonstration reproduced the apostrophe error and showed that the unsafe payload returned all 2,000 customers. Bound parameters treated the payload as data and correctly handled a name containing an apostrophe.

## Run from the repository root

```powershell
python Module03/bench.py
python Module03/injection_demo.py
```

Only Python's standard library is required. The Python and SQLite versions are recorded in [results.json](results.json).

The benchmark rebuilds **Module03/warehouse.db** and overwrites the generated benchmark reports. It uses an in-memory copy of the Module02 setup for the plan safari and does not modify Module02/legacy.db.

Timings can vary between runs. Compare the actual query plans as well as the measured times.

## Optional SQLite CLI commands

```powershell
sqlite3 Module03/warehouse.db ".read Module03/setup.sql"
sqlite3 Module03/warehouse.db ".read Module03/queries.sql"
```

Running setup recreates the tables and removes their indexes. Run bench.py again for the complete index comparison.

## Next steps

- Practise explaining the query plans and bound parameters independently.
- Write an independent relational-algebra expression and compare it with the AI-assisted version.
- Compare query plans and SQLite versions with another pod.
- Record the actual feedback received during the practice round.