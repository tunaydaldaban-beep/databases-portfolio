# Module 2 study preparation

**Status:** AI-prepared reference notes and verified technical examples. They are not a record of Tunay having studied, searched, met a pod or posted in Discord. Personal entries below remain pending.

## References consulted during preparation

| Source | Concept illustrated |
|---|---|
| [Professor's Module 2 workbook](https://github.com/iotempire/iotempire-teaching/blob/main/full-classes/hsbi-databases-10d/modules/02-data-contracts-and-legacy-schemas.md) | Reconstruct intended relationships from broken maintenance data; content below its draft boundary is provisional |
| [SQLite foreign keys](https://www.sqlite.org/foreignkeys.html) | Child-to-parent checks, NULL optionality and connection-level enforcement |
| [Mermaid ER diagrams](https://mermaid.js.org/syntax/entityRelationshipDiagram.html) | Crow's-foot minimum/maximum participation and PK/FK notation |
| [Pydantic validators](https://docs.pydantic.dev/latest/concepts/validators/) | Field validation and custom rules before persistence |
| [SQLAlchemy SQLite dialect](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html) | SQLite constraints and enabling foreign keys on connection |

## Research questions and verified answers

These are preparation questions, not a fabricated personal search history.

- **Where does the FK go in 1:n?** On the child/many side. SQLite's artist/track example and [the sensor proof](sketch-proof-results.txt) show multiple children referencing one parent.
- **Does a natural key become a key merely by being named part_no?** No. P-1003 occurs twice; the proposed PK rejects duplicates. See [audit](integrity-results.txt) and [tests](test-results.txt).
- **Does a numeric declaration enforce money rules in SQLite?** No. Numeric affinity is not a complete financial contract; explicit checks and Decimal validation are used. See [business rules](business-rules.md).
- **Is a job just a relationship?** It is useful as an event entity with its own ID and date. It links Machine and Technician and participates in JobPart.
- **What does EER add?** Generalization/specialization, such as Machine with CNC and injection-molder subtypes. Disjoint means an instance cannot belong to both; complete means every parent belongs to a subtype. Ordinary ER/FK diagrams alone do not prove either condition.

## Remarkable technical findings to discuss

The naive part join both drops job 1 and duplicates job 2. A date-shaped string can be invalid. A count of three names is not proof of three distinct people. A mandatory child FK does not force a parent to have children. These are verified/modeling observations, not claimed personal reactions.

## LLM Q&A and verification

The following requests are taken from the supplied master prompt and answered in this implementation; no separate external LLM conversation is claimed.

| Prompt/request | Answer summary | Verification and limits |
|---|---|---|
| Distinguish a database rule of “at most one” from the business requirement “exactly one.” | A shared child PK/FK limits children to one but does not require a child for each parent. | Review the nameplate key placement in [four examples](er-examples.md); do not overclaim FK coverage. |
| Also document how duplicate parts can produce duplicated join results. | Both P-1003 rows match job 2, so the result contains it twice. | Actual [integrity results](integrity-results.txt). |
| Be careful with SQLite type affinity: declaring a column NUMERIC alone does not guarantee every inserted value has correct money semantics. | Use Decimal input validation and explicit database checks; exact arithmetic needs a stronger representation. | Negative, text and fractional-cent insertion tests; documented floating-point limitation. |

## Two sourced example redraws

### 1. Artist and Track — SQLite example

Source: [SQLite foreign-key documentation, introductory artist/track example](https://www.sqlite.org/foreignkeys.html). This is an original redraw of the source schema. The required parent below is an explicit adaptation: SQLite's initial nullable trackartist example allows an absent artist; adding NOT NULL changes it to exactly one for each track.

```mermaid
erDiagram
    ARTIST ||..o{ TRACK : records
    ARTIST {
        int artistid PK
        string artistname
    }
    TRACK {
        int trackid PK
        string trackname
        int trackartist FK
    }
```

Teaching point: FK existence and NOT NULL answer different questions. A parent can have no tracks. Tunay's own takeaway: **PENDING**.

### 2. Property and Room — Mermaid example

Source: [Mermaid ER documentation](https://mermaid.js.org/syntax/entityRelationshipDiagram.html), PROPERTY/ROOM example. The IDs and address shown here are illustrative additions to make key placement explicit.

```mermaid
erDiagram
    PROPERTY ||..|{ ROOM : contains
    PROPERTY {
        int property_id PK
        string address
    }
    ROOM {
        int room_id PK
        int property_id FK
    }
```

Teaching point: one-or-more participation can be drawn, but a room FK cannot require each property to contain a room. Tunay's own comparison with the first example: **PENDING**.

## Task B — four own examples and proof

See [er-examples.md](er-examples.md), [SQL proof](sketch-proof.sql) and [executed proof](sketch-proof-results.txt). Review the difference between intended requirements and enforced constraints before explaining the diagrams.

## Task A — personal study record

**PENDING — TUNAY'S PERSONAL INPUT**

- Actual study date, duration and participants:
- Sources I personally consulted and the concept each clarified:
- Questions I searched and the sources I used:
- What surprised me, and what is still unclear:
- My explanation of the two selected sketches:

## Agreed learning (pod discussion)

**PENDING — actual discussion required.** Record the date, participants, neighboring pod, 3–5 agreed points, remaining disagreement and how feedback changed the diagrams. Prior Module 1 Zoom discussion is not evidence of this Module 2 activity.

Possible discussion questions (proposals, not agreed results): Why is P-1003 not currently a key? Why does job 1 disappear? Which checks belong in the database? What would enforce exactly one nameplate? How would we distinguish technicians with the same name?

## Task C — shared image

**PENDING — choose one image together and post it in the class Discord channel.** Candidate: [rendered corrected model](pictures/corrected-er.png) ([source](pictures/corrected-er.mmd)). Record the real post link/date, chosen image and one-sentence explanation here. No message has been sent on Tunay's behalf.
