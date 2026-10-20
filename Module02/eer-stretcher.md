# Optional Task 4 — EER inheritance

[Executable alternatives](eer-stretcher.sql) · [Proof runner](run_stretchers.py) · [Actual evidence](eer-results.txt)

Run: `uv run python Module02/run_stretchers.py`

| Issue | Single table with discriminator | Base and separate subtype tables |
|---|---|---|
| Simplicity | One insert/query | Joins and transactional multi-table inserts |
| Nullability | Irrelevant fields NULL; CHECK enforces required relevant fields | Subtype payload NOT NULL |
| Referential integrity | Single machine identity | Subtype FK references (machine_id, kind) |
| Disjointness | Allowed kind plus mutually exclusive payload CHECK | Fixed subtype kind and composite FK prevent the same base ID belonging to both subtypes |
| Completeness | Each row must contain its selected subtype payload | NOT guaranteed: a base row can exist without a subtype row |
| Extensibility | Add columns and adjust CHECK when adding types | Add tables, update accepted kinds and workflow |

**Decision:** I would recommend the single-table design for these two small, stable subtypes because it enforces disjointness and completeness within one row with simple inserts. This is an AI-prepared design recommendation for Tunay to review, not a claimed personal decision from his study.

The tests deliberately accept base ID 2 without a subtype in the second design. A workflow must create/check the subtype in the same transaction before completing a machine record; an ordinary child-to-parent FK cannot enforce parent-to-child existence. For many large or independently evolving subtypes, separate tables can justify that extra complexity. Neither model is added to the core maintenance contract.
