# Module 02 — Data Contracts & Legacy Schema Audits

Student: Tunay Daldaban · HSBI Industrial Engineering

**Status: core technical implementation prepared and tested with AI assistance; personal study, discussion and reflection remain pending.** Execution evidence was generated in the assistant's Linux environment. Tunay must review it and rerun locally before claiming personal execution.

## Learning goals and evidence

| Goal | Evidence |
|---|---|
| Reconstruct an ER/EER model | [ER audit](er-audit.md), [four relationship sketches](er-examples.md) |
| Prove integrity defects with queries | [Five defects and impacts](integrity-audit.md), [SQL](integrity-audit.sql), [results](integrity-results.txt) |
| Explain entities, attributes and key choices | [ER audit](er-audit.md), [study notes](study-log.md) |
| Build a code-first contract | [Pydantic/SQLAlchemy](contract.py), [emitted DDL](corrected-schema.sql), [tests](tests/test_contract.py) |
| Recover missing business rules | [Enforcement and limits](business-rules.md) |

## Reproduce from the repository root (PowerShell)

```powershell
uv sync --frozen
uv run python Module02/run_audit.py
uv run python Module02/contract.py
uv run python -m unittest discover -s Module02/tests -v
```

The audit runner recreates only `Module02/legacy.db` from the deliberately flawed [fixture](legacy_setup.sql), runs the saved SQL queries and proof, and refreshes evidence files. Corrected-schema tests use isolated in-memory databases. Generated `.db` files are ignored by Git. The new schema uses five tables, including a separate Technician entity; no automatic repair migration is claimed.

## Evidence index

- [Study preparation and pending pod record](study-log.md)
- [Cardinality queries](cardinality-audit.sql) and [results](cardinality-results.txt)
- [Sketch SQL proof](sketch-proof.sql) and [results](sketch-proof-results.txt)
- [Environment](environment.txt) and [25-test results](test-results.txt)
- [Optional EER inheritance comparison](eer-stretcher.md)
- [Personal reflection draft](../Reflections/ref02.md)
- [Technical completion report](technical-completion-report.md)
- [Professor's workbook](https://github.com/iotempire/iotempire-teaching/blob/main/full-classes/hsbi-databases-10d/modules/02-data-contracts-and-legacy-schemas.md)
- Pod mate: [İsa Babayev's portfolio](https://github.com/isa-babayev-ibabayev/databases-portfolio)

## Before academic submission

Study and explain the four diagrams; rerun and inspect the evidence; write your own reflection; complete the neighboring-pod discussion; record 3–5 real agreed lessons and any disagreement; choose and share one image in Discord. No peer review, pod meeting or Discord post is claimed by this implementation.
