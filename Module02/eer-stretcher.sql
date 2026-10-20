-- Alternative A: complete and disjoint subtype selection in one row.
PRAGMA foreign_keys=ON;
CREATE TABLE machine_single (
 machine_id INTEGER PRIMARY KEY,
 kind TEXT NOT NULL CHECK(kind IN ('cnc','injection')),
 axes INTEGER,
 clamp_tonnes REAL,
 CHECK((kind='cnc' AND axes IS NOT NULL AND axes>=1 AND clamp_tonnes IS NULL)
    OR (kind='injection' AND clamp_tonnes IS NOT NULL AND clamp_tonnes>0 AND axes IS NULL))
);
-- Alternative B: separate subtype payloads, with a composite FK fixing subtype.
CREATE TABLE machine_base (
 machine_id INTEGER PRIMARY KEY,
 kind TEXT NOT NULL CHECK(kind IN ('cnc','injection')),
 UNIQUE(machine_id,kind)
);
CREATE TABLE cnc_machine (
 machine_id INTEGER PRIMARY KEY,
 kind TEXT NOT NULL DEFAULT 'cnc' CHECK(kind='cnc'),
 axes INTEGER NOT NULL CHECK(axes>=1),
 FOREIGN KEY(machine_id,kind) REFERENCES machine_base(machine_id,kind)
);
CREATE TABLE injection_machine (
 machine_id INTEGER PRIMARY KEY,
 kind TEXT NOT NULL DEFAULT 'injection' CHECK(kind='injection'),
 clamp_tonnes REAL NOT NULL CHECK(clamp_tonnes>0),
 FOREIGN KEY(machine_id,kind) REFERENCES machine_base(machine_id,kind)
);
