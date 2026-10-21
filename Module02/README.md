# Module 02 — Data Contracts & Legacy Schema Audits

Student: Tunay Daldaban · HSBI Industrial Engineering

**Status:** Core technical implementation completed and verified locally on Windows. All 25 automated tests and the optional EER checks passed. The implementation, local execution results and personal reflection have been pushed to GitHub.

The work was prepared with AI assistance. I discussed the module briefly with my groupmate, İsa Babayev. Initial personal study notes have been added. Individual takeaways from the two sourced ER examples, the neighboring-pod discussion and the Discord image share remain pending.

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
uv run python Module02/run_stretchers.py
```

The audit runner recreates `Module02/legacy.db` from the deliberately flawed fixture and refreshes the evidence files. Contract tests use isolated in-memory databases. Generated database files are ignored by Git.

The corrected schema uses five tables, including a separate Technician entity. No automatic migration of the defective legacy data is implemented.

## Evidence index

- [Study notes and pending pod record](study-log.md)
- [Legacy setup script](legacy_setup.sql)
- [Cardinality queries](cardinality-audit.sql) and [results](cardinality-results.txt)
- [Integrity queries](integrity-audit.sql) and [results](integrity-results.txt)
- [Sketch SQL proof](sketch-proof.sql) and [results](sketch-proof-results.txt)
- [Windows environment](environment.txt) and [25-test results](test-results.txt)
- [Optional EER inheritance comparison](eer-stretcher.md)
- [Personal reflection](../Reflections/ref02.md)
- [Technical completion report](technical-completion-report.md)
- [Professor's workbook](https://github.com/iotempire/iotempire-teaching/blob/main/full-classes/hsbi-databases-10d/modules/02-data-contracts-and-legacy-schemas.md)
- Pod mate: [İsa Babayev's portfolio](https://github.com/isa-babayev-ibabayev/databases-portfolio)

## Remaining activities

- Complete personal takeaways from the two sourced ER examples.
- Review and explain the four relationship sketches and their constraints.
- Complete the neighboring-pod discussion and record 3–5 agreed lessons.
- Choose and share one image in the class Discord channel.

The technical completion report records the original preparation stage; its delivery and personal-progress information still needs updating.