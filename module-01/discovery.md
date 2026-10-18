# Embedded versus client/server

| Question | Embedded | Client/server |
|---|---|---|
| Where does it run? | Inside the application's process | In a separate database server process |
| Examples | SQLite, DuckDB | PostgreSQL, MySQL |
| Advantage | Direct local access, no separate database service, offline operation | Central access and coordination for many clients |
| Cost/trade-off | Concurrency and sharing must suit the engine and workload | Service configuration, authentication, maintenance and network handling |
| Typical fit | SQLite for local operational storage; DuckDB for local analytical queries | Shared applications with many simultaneous writers |

SQLite allows many readers but only one active writer at a time; do not assume this exact rule describes every embedded engine. An embedded database still needs backups and can fail due to disk, process or permission problems. “No server” does not mean “cannot fail.”

The telemetry script opens a local SQLite file directly and executes SQL without starting a database server or connecting to a network endpoint. Actual size, row count and timings appear in [query-results.md](query-results.md). This demonstrates that this exercise fits locally; it is not a measured comparison with PostgreSQL.

Cloud cost sentence: a hosted design can introduce compute, storage, backup and administration costs paid by the machine-shop operator; no price is asserted without a provider and configuration. Local storage also has hardware and backup costs.

Useful dot-command: `.schema` displays the table definition, helping check column names and types before writing a query.
