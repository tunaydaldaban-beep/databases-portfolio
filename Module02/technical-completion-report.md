# Module 2 — Technical completion report

## Current status update — 22 October 2026

This update supersedes the delivery and personal-progress statements in the original report below.

- The implementation was transferred to my Windows computer and successfully pushed to GitHub.
- I ran `Module02/run_audit.py`: all 25 tests passed, along with the fixture, audit, sketch and DDL checks.
- I also ran `Module02/run_stretchers.py`; all reported checks passed.
- Windows execution evidence was committed in `d1c8bdf`.
- My personalized reflection was published in `3516e3c`.
- Initial personal study notes were published in `c382db8`.
- The Module 2 README evidence links and instructions were restored in `4b9b0cb`.
- I had a brief discussion with İsa Babayev. This was not the neighboring-pod activity required by Task C.

Remaining work: individual takeaways from the two sourced ER examples, review and explanation of the diagrams, the neighboring-pod discussion, 3–5 agreed lessons and the Discord image share.

**Overall status: technical work verified locally and published; some learning and collaboration activities remain pending.**

The sections below describe the original preparation and verification stage.

## A. Executive summary

The core technical work from the supplied Module 2 workbook is implemented: the original broken fixture, four ER sketches, one executable cardinality proof, reconstructed maintenance model, five SQL defect demonstrations, Pydantic/SQLAlchemy contract, generated DDL and 25 automated contract tests. Optional EER Task 4 is also implemented and executed. Personal study, understanding, neighboring-pod discussion, Discord sharing and reflection remain pending.

All recorded execution in this delivery is assistant execution on Linux on 2026-10-20, not a claim that Tunay ran these commands. No academic completion or human participation is fabricated. The professor's workbook labels its detailed activities as provisional below a draft boundary.

## B. Repository identity and delivery

- Repository: https://github.com/tunaydaldaban-beep/databases-portfolio
- Verified local root: `/workspace/scratch/13f9562d8d87/module2-work`
- Branch: `main`; remote `origin` points to Tunay's repository above.
- Starting commit: `4abaee910a43267f1e80c6fda2c6f81343820278`.
- Initial working tree: clean, tracking `origin/main`.
- Final delivery commit: supplied in the final delivery message after committing; no self-referential hash is invented here.
- Push and synchronization: Blocked: `git push origin main` failed with `could not read Username for https://github.com`. Local commits are retained. A patch package and PowerShell delivery instructions are provided; the repository is not synchronized with these new commits.
- Existing configured Git author identity is preserved. No force push or history rewriting is used.

## C. Environment

[Actual environment output](environment.txt): Python 3.14.8, SQLite 3.53.1, Pydantic 2.14.1, SQLAlchemy 2.1.5, Linux x86_64. `uv --version`: 0.12.23. `uv sync --frozen` used the repository's unchanged lockfile and Python 3.14.8. Node v24.19.0 was used for external diagram verification tooling, not as a project dependency.

## D. Module 1 preservation

`git diff 4abaee910a43267f1e80c6fda2c6f81343820278 -- module-01` returned no output. No Module 1 file, database or evidence was modified. Outside Module02, only `Reflections/ref02.md` is created (the professor's required path) and the root README's Module 2 label changes from “upcoming” to “technical evidence ready; personal activities pending.” The original Python project configuration, dependency lock and ignore rules remain unchanged. Generated databases and virtual environments are not committed.

## E. Requirement-by-requirement matrix

PASS below means technical evidence exists and was verified, not that student competency or participation has been assessed.

| Professor requirement | Evidence | Verification | Status |
|---|---|---|---|
| Learning Goal 1: reconstruct ER/EER model | [ER audit](er-audit.md), [EER comparison](eer-stretcher.md) | Attribute/key review, actual counts, subtype SQL proof | PASS technical |
| Learning Goal 2: prove integrity defects | [Defect audit](integrity-audit.md), [results](integrity-results.txt) | Five queries executed and expected rows asserted | PASS technical |
| Learning Goal 3: entities/attributes and key choices | [Four examples](er-examples.md), [ER audit](er-audit.md) | Key-placement and identity rationale documented | PASS technical; student explanation pending |
| Learning Goal 4: code-first contract | [Code](contract.py), [DDL](corrected-schema.sql) | DDL rebuilt in fresh memory DB; 25 tests | PASS technical |
| Learning Goal 5: missing requirements | [Business rules](business-rules.md) | Application/database/process mapping reviewed against implementation | PASS technical |
| Task A: study log, sources, Q&A, two found sketches | [Study log](study-log.md) | Sources and adapted redraws prepared; no personal study asserted | PARTIAL |
| Task B: four sketches and one SQL proof | [Examples](er-examples.md), [proof output](sketch-proof-results.txt) | Two children share a parent; invalid parent rejected | PASS technical; explanation pending |
| Task C: neighboring pod and Discord | [Pending record](study-log.md#agreed-learning-pod-discussion) | No meeting/post evidence available | PENDING |
| Studio Task 1 | [ER audit](er-audit.md), [counts](cardinality-results.txt) | Counts establish observed multiplicities, not universal limits | PASS |
| Studio Task 2 | [Queries](integrity-audit.sql), [impacts](integrity-audit.md) | Exact results saved and verified | PASS |
| Studio Task 3 | [Contract](contract.py), [rules](business-rules.md) | Valid/invalid models and database constraints exercised | PASS |
| Reflection | [Required reflection path](../Reflections/ref02.md) | Professor template headings; honest technical draft | PARTIAL — personal input pending |
| Optional Task 4 | [Alternatives](eer-stretcher.sql), [results](eer-results.txt) | 11 executed acceptance/rejection/assertion outcomes | PASS technical |
| Optional Task 5 | Not implemented as a full exercise | Three-example curation and schema/diagram round-trip not delivered | OPTIONAL — NOT DONE |

## F. Created and modified files

- `README.md` — Module 2 evidence index and reproduction instructions.
- `legacy_setup.sql` — Original deliberately flawed fixture.
- `cardinality-audit.sql` — Counts and list-splitting queries.
- `cardinality-results.txt` — Actual count results.
- `integrity-audit.sql` — Five defect queries and numeric comparison.
- `integrity-results.txt` — Actual defect query output.
- `integrity-audit.md` — Production impacts and repair decisions.
- `er-examples.md` — Four Task B sketches and rationale.
- `er-audit.md` — Reconstructed entities, keys and measured cardinalities.
- `sketch-proof.sql` — Machine/sensor schema and count demonstration.
- `sketch-proof-results.txt` — Actual proof and orphan rejection.
- `contract.py` — Pydantic and SQLAlchemy contract.
- `corrected-schema.sql` — Generated buildable SQLite DDL.
- `business-rules.md` — Rule enforcement and limits.
- `run_audit.py` — Reproducible fixture, SQL, DDL and test runner.
- `environment.txt` — Actual runtime versions.
- `tests/test_contract.py` — 25 isolated contract tests.
- `test-results.txt` — Actual unittest output.
- `study-log.md` — Sources, verified Q&A, two redraws and human placeholders.
- `eer-stretcher.sql` — Two optional inheritance designs.
- `eer-stretcher.md` — Design trade-offs.
- `run_stretchers.py` — Optional EER verification.
- `eer-results.txt` — Actual optional outcomes.
- `pictures/*.mmd` — Seven Mermaid sources matching the Markdown diagrams.
- `pictures/*.png` — Seven rendered diagrams, including a candidate Discord image.
- `diagram-verification.txt` — Actual renderer verification.
- `../Reflections/ref02.md` — Required reflection draft with personal fields pending.
- `../README.md` — Update only Module 2 progress label.
- `technical-completion-report.md` — This requirement-by-requirement delivery report.

The pre-existing `Module02/pictures/README.md` is preserved. Database `.db` files and `.venv` are local rebuildable outputs, not delivery artifacts.

## G. Commands executed and reproduction

From the repository root, the following commands were actually executed during implementation and fresh verification; the commands also work in PowerShell:

```powershell
uv --version
uv sync --frozen
uv run python Module02/run_audit.py
uv run python Module02/contract.py
uv run python -m unittest discover -s Module02/tests -v
uv run python Module02/run_stretchers.py
```

`run_audit.py` reconstructs `Module02/legacy.db` from `legacy_setup.sql`, executes both audit SQL files, writes both result files, runs the sketch proof in a separate in-memory database, emits and reconstructs corrected DDL, records versions, and runs the tests. This is the recommended Windows path and does not require shell heredocs. It deliberately replaces the Module02 fixture tables and evidence outputs; do not store personal data in this exercise database.

To inspect individual audit files with an already installed SQLite CLI, these additional PowerShell commands are provided as instructions (not claimed executed in this Linux run):

```powershell
sqlite3 Module02/legacy.db ".read Module02/cardinality-audit.sql"
sqlite3 Module02/legacy.db ".read Module02/integrity-audit.sql"
```

The contract command writes `Module02/corrected-schema.sql` itself. Do not pipe output back onto its source filename. Generated corrected tables are exercised in fresh, isolated memory databases; the original fixture is never “fixed” to hide defects.

## H. Database results and corrections

Legacy table counts: machine 4, part 4, maint_job 4. There are 3 distinct part numbers and 3 distinct technician strings. cnc-01 has 2 jobs; cnc-02 and missing cnc-05 have 1 each. Jobs 1–4 have 2, 1, 1, 0 parts. P-1001 appears in 2 jobs, showing multiplicity in the other direction too.

| Defect | Actual result | Correction |
|---|---|---|
| Orphan | job 3 → cnc-05 | Reconcile/quarantine and use required FK |
| Duplicate part | P-1003 → 2 copies | Reconcile and enforce natural PK |
| Text prices | Lexical filter returns only P-1001; numeric filter also returns two P-1003 rows | Decimal input validation plus numeric storage/checks |
| Invalid date | RANDOM-NAME → unknown | Obtain date/agree policy; real-date validation |
| List join | job 1 lost, job 2 repeated, job 3 returned once | Normalized job_part with FKs and composite PK |

[Exact statements and outputs](integrity-results.txt) and [counts](cardinality-results.txt) accompany the written conclusions. The original NULL-sensitive part-count expression is retained alongside a corrected CASE expression. Migration decisions are explicitly unresolved; no missing machine or date is invented.

## I. Pydantic and SQLAlchemy contract

Application models: Machine, Part, Technician and MaintenanceJob. They validate strict positive IDs, serial/part prefixes, nonblank text, real dates, finite nonnegative prices with two decimal places, and duplicate-free lists of part numbers.

Database tables: machine, part, technician, maint_job and job_part. Machine serials are UNIQUE; part numbers are natural primary keys; jobs reference a required machine and technician; the junction composite PK prevents repeated job/part pairs. SQLAlchemy connection hooks enable foreign keys. Additional SQLite CHECKs constrain text shape, positive PKs and price storage/range/cent precision.

A separate Technician table intentionally extends the workbook's short sample. Pydantic does not perform parent existence or uniqueness lookups. Database FKs/keys handle those. Date shape is weaker than calendar validity, and SQLite NUMERIC affinity is weaker than exact decimal arithmetic. See [full enforcement matrix](business-rules.md).

## J. Genuine verification results

- **25 unittest tests passed, 0 failed, 0 errors**; [raw output](test-results.txt). Subtests for bad price variants are included inside one test, not inflated into extra test counts.
- Fixture rebuild, five-table DDL reconstruction, exact defect-output assertions and sensor FK rejection passed in `run_audit.py`.
- Optional inheritance proof: 11 explicit successful outcomes, including an accepted missing-subtype counterexample. These are separate from the 25 unittest tests.
- Workflow was rerun after implementation against a freshly reconstructed fixture; contract databases are new per test.
- Local Markdown links were checked against existing files. External links and live GitHub visual rendering were not exhaustively verified.
- Seven Mermaid diagrams were rendered to PNG using Mermaid CLI with Chromium; the corrected model was visually inspected. The initial default browser download failed (proxy timeout); rendering succeeded with a packaged Chromium executable. See [render log](diagram-verification.txt).
- Git protection check: Module 1 unchanged; no generated DB, venv or credentials staged.

## K. Optional exercises

Task 4: both single-table and separate-subtype SQL designs implemented. Single-table checks enforce complete, disjoint subtype payloads. Composite FKs enforce disjoint subtype identity in the multi-table alternative, but do not force every base row to have a child; the executed counterexample records that limit. Recommendation and trade-offs are documented.

Task 5 is not claimed complete. The core work includes Mermaid sources and two sourced redraws, but that does not substitute for the optional three-example collection, full schema/diagram round-trip, critique and sharing activity.

## L. Human activities pending

1. Tunay studies the ER/EER concepts and adds genuine sources, questions and learning notes.
2. Review and explain the four diagrams, key decisions and at-most-one versus exactly-one distinction.
3. Rerun locally and inspect the SQL results and failed-insert examples; record only checks actually performed.
4. Complete the reflection in Tunay's own words.
5. Discuss with the Task Pod and a neighboring pod; document actual participants, date, 3–5 agreed lessons and remaining disagreements.
6. Choose one diagram together and post it in the class Discord channel, then record real evidence.
7. Provide any checkpoint/peer-review evidence requested by the instructor; no review or comment is manufactured here.

## M. Known issues, assumptions and limits

- One technician per job, stable part codes, nonnegative two-decimal prices and optional zero parts per job are explicit exercise assumptions.
- No migration, CRUD persistence layer, quantities, currencies or historical pricing is implemented.
- SQLite price checks use a floating-point tolerance; integer minor units are preferable if exact money storage is required.
- Direct SQL calendar validation and parent-minimum participation are not fully enforced; application/process requirements are documented.
- Windows commands are provided, but this delivery was executed on Linux. Tunay's local Windows execution remains unverified.
- Workbook content below its draft boundary may change; requirements are based on the supplied snapshot.
- Rendering/deployment details and any delivery limitation are stated above; no live GitHub visual inspection is inferred from a local render.

## N. Overall status

**Core technical implementation complete; human activities pending.** Optional Task 4 is delivered; optional Task 5 is not. This report is prepared for independent comparison with the professor's workbook and does not certify Tunay's personal completion.
