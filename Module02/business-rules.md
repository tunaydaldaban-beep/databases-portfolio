# Requirements the legacy schema forgot

| Requirement | Pydantic / application | Database | Remaining decision or limit |
|---|---|---|---|
| Unique serial numbers | Prefix and nonblank suffix | UNIQUE, NOT NULL, prefix/length check | Direct SQLite LIKE is case-insensitive by default; application prefix is case-sensitive |
| Positive identifiers | Strict positive integers | Positive PK CHECKs; required FKs reference parents | SQLite can generate an INTEGER PK if omitted; application requires an ID |
| Existing machine and technician for each job | Accepts typed IDs, does not look up parents | NOT NULL FKs, enabled per connection | Direct connections must also enable foreign_keys |
| Unique part number | Prefix validation | PK and NOT NULL | Part-code stability is a design assumption |
| Suitable prices | Finite Decimal, nonnegative, at most 9 digits and 2 decimal places | Numeric affinity plus numeric storage class, range and cent-tolerance CHECK | SQLite NUMERIC(9,2) alone is insufficient; for strict financial arithmetic prefer integer minor units and a currency policy |
| Valid dates | Real calendar date validation | ISO text shape CHECK and NOT NULL | Direct SQL can still insert impossible calendar dates; calendar validity is an application rule |
| Multiple parts per job | list of part numbers | job_part junction table | Persistence must map the validated list to junction rows in a transaction |
| No repeated part in one job | List duplicate validator | Composite PK (job_id, part_no) | Quantity is not modeled; add quantity if repeated units are required |
| Technician identity | Separate typed technician ID and nonblank name | technician PK, name NOT NULL | Same name can belong to different people; identity reconciliation is a business process |
| Required descriptions and site | Strip whitespace, require nonempty text | NOT NULL and trim-length CHECK | Accepted sites/catalogue values not specified |
| Job date compatible with installation | Not currently checked | Not currently checked | Clarify whether pre-installation work is valid; cross-table rule needs workflow/trigger |

Pydantic gives early, readable input errors; database constraints protect against independent writers. Neither alone proves a workflow is correct. This implementation provides validation and DDL, not a complete CRUD service or a repair migration. Historical prices, currencies, quantities, multiple technicians and deletion policy need explicit requirements. Existing referenced parents are protected by default foreign-key NO ACTION behavior.
