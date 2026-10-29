# Plan safari, covering indexes and rewrites

Predictions were recorded in [predictions.md](predictions.md) before execution.

## Safari before

```sql
SELECT * FROM maint_job WHERE technician='Beier';
```
```text
SCAN maint_job
```

## Safari before

```sql
SELECT * FROM machine WHERE machine_name='cnc-02';
```
```text
SCAN machine
```

## Safari before

```sql
SELECT * FROM maint_job WHERE technician LIKE '%ei%';
```
```text
SCAN maint_job
```

## Safari before

```sql
SELECT * FROM maint_job WHERE lower(technician)='beier';
```
```text
SCAN maint_job
```

## Safari after

```sql
SELECT * FROM maint_job WHERE technician='Beier';
```
```text
SEARCH maint_job USING INDEX ix_job_tech (technician=?)
```

## Safari after

```sql
SELECT * FROM machine WHERE machine_name='cnc-02';
```
```text
SCAN machine
```

## Safari after

```sql
SELECT * FROM maint_job WHERE technician LIKE '%ei%';
```
```text
SCAN maint_job
```

## Safari after

```sql
SELECT * FROM maint_job WHERE lower(technician)='beier';
```
```text
SCAN maint_job
```

## Covering demo

```sql
SELECT a FROM t WHERE a=1;
```
```text
SEARCH t USING COVERING INDEX i (a=?)
```

## Covering demo

```sql
SELECT a,b FROM t WHERE a=1;
```
```text
SEARCH t USING INDEX i (a=?)
```

## grouped rewrite

```sql
SELECT c.customer_id,c.name,COUNT(*) AS late_orders FROM orders o JOIN customer c ON c.customer_id=o.customer_id WHERE o.status='late' GROUP BY c.customer_id,c.name ORDER BY late_orders DESC,c.customer_id;
```
```text
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR ORDER BY
```
Rows: 400; first rows: [(1, 'Customer 1', 30), (6, 'Customer 6', 30), (11, 'Customer 11', 30)]

## correlated rewrite

```sql
SELECT c.customer_id,c.name,(SELECT COUNT(*) FROM orders o WHERE o.customer_id=c.customer_id AND o.status='late') AS late_orders FROM customer c WHERE EXISTS(SELECT 1 FROM orders o WHERE o.customer_id=c.customer_id AND o.status='late') ORDER BY late_orders DESC,c.customer_id;
```
```text
SCAN c
BLOOM FILTER ON o (customer_id=? AND status=?)
SEARCH o EXISTS USING AUTOMATIC PARTIAL COVERING INDEX (customer_id=? AND status=?)
CORRELATED SCALAR SUBQUERY 1
SCAN o
USE TEMP B-TREE FOR ORDER BY
```
Rows: 400; first rows: [(1, 'Customer 1', 30), (6, 'Customer 6', 30), (11, 'Customer 11', 30)]

## window rewrite

```sql
SELECT DISTINCT c.customer_id,c.name,COUNT(*) OVER(PARTITION BY c.customer_id) AS late_orders FROM orders o JOIN customer c ON c.customer_id=o.customer_id WHERE o.status='late' ORDER BY late_orders DESC,c.customer_id;
```
```text
CO-ROUTINE (subquery-2)
CO-ROUTINE (subquery-3)
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR ORDER BY
SCAN (subquery-3)
SCAN (subquery-2)
USE TEMP B-TREE FOR DISTINCT
USE TEMP B-TREE FOR ORDER BY
```
Rows: 400; first rows: [(1, 'Customer 1', 30), (6, 'Customer 6', 30), (11, 'Customer 11', 30)]

All rewrites return the same rows, excluding customers with zero late orders. The grouped query is the default AI-assisted choice and simplest to read. The correlated version repeats work per customer and has no customer_id index here. The window version preserves rows before DISTINCT removes duplicates. Secondary customer_id ordering makes tied counts deterministic.
