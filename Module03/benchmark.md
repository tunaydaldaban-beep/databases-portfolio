# Measured query plans and benchmark

Python 3.14.8; SQLite 3.53.1. Executed locally on Tunay's Windows computer.

Run `python Module03/bench.py` from the repository root to regenerate. Rebuilds only Module03/warehouse.db. All times are milliseconds per fully fetched query; warm-up plus median of 3 samples; 30-query batches for short queries. Same connection, no ANALYZE. Timings include Python overhead and warm caches. See [raw samples](results.json).

| Stage | Dashboard ms | Single-day ms | Wrapped date ms | Product filter ms |
|---|---:|---:|---:|---:|
| baseline | 192.272 | 3.505 | 8.132 | 8.745 |
| date only | 101.945 | 0.146 | 6.809 | 8.633 |
| order only | 104.739 | 3.031 | 5.529 | 8.577 |
| product only | 112.914 | 3.039 | 5.626 | 1.253 |
| date + order | 868.982 | 0.154 | 5.196 | 8.151 |
| all three | 802.751 | 0.165 | 5.170 | 1.302 |

## Dashboard result

| City | Distinct customers | Revenue |
|---|---:|---:|
| Bielefeld | 500 | 11242176.00 |
| Gütersloh | 500 | 8422344.00 |
| Münster | 500 | 5493504.00 |
| Paderborn | 500 | 2815656.00 |

## Exact plans

### baseline / dashboard

```text
SCAN ol
SEARCH o USING INTEGER PRIMARY KEY (rowid=?)
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
SEARCH p USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR count(DISTINCT)
USE TEMP B-TREE FOR ORDER BY
```

### baseline / single_day

```text
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

### baseline / wrapped_date

```text
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

### baseline / product_filter

```text
SCAN order_line
```

### date only / dashboard

```text
SCAN ol
SEARCH o USING INTEGER PRIMARY KEY (rowid=?)
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
SEARCH p USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR count(DISTINCT)
USE TEMP B-TREE FOR ORDER BY
```

### date only / single_day

```text
SEARCH o USING INDEX ix_orders_ordered_on (ordered_on=?)
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

### date only / wrapped_date

```text
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

### date only / product_filter

```text
SCAN order_line
```

### order only / dashboard

```text
SCAN ol
SEARCH o USING INTEGER PRIMARY KEY (rowid=?)
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
SEARCH p USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR count(DISTINCT)
USE TEMP B-TREE FOR ORDER BY
```

### order only / single_day

```text
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

### order only / wrapped_date

```text
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

### order only / product_filter

```text
SCAN order_line
```

### product only / dashboard

```text
SCAN ol
SEARCH o USING INTEGER PRIMARY KEY (rowid=?)
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
SEARCH p USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR count(DISTINCT)
USE TEMP B-TREE FOR ORDER BY
```

### product only / single_day

```text
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

### product only / wrapped_date

```text
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

### product only / product_filter

```text
SEARCH order_line USING INDEX ix_orderline_product (product_id=?)
```

### date + order / dashboard

```text
SEARCH o USING INDEX ix_orders_ordered_on (ordered_on>? AND ordered_on<?)
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
SEARCH ol USING INDEX ix_orderline_order (order_id=?)
SEARCH p USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR count(DISTINCT)
USE TEMP B-TREE FOR ORDER BY
```

### date + order / single_day

```text
SEARCH o USING INDEX ix_orders_ordered_on (ordered_on=?)
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

### date + order / wrapped_date

```text
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

### date + order / product_filter

```text
SCAN order_line
```

### all three / dashboard

```text
SEARCH o USING INDEX ix_orders_ordered_on (ordered_on>? AND ordered_on<?)
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
SEARCH ol USING INDEX ix_orderline_order (order_id=?)
SEARCH p USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR count(DISTINCT)
USE TEMP B-TREE FOR ORDER BY
```

### all three / single_day

```text
SEARCH o USING INDEX ix_orders_ordered_on (ordered_on=?)
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

### all three / wrapped_date

```text
SCAN o
SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

### all three / product_filter

```text
SEARCH order_line USING INDEX ix_orderline_product (product_id=?)
```

## Verification

- PASS: Row counts
- PASS: Results unchanged across all index stages
- PASS: Independent Python dashboard calculation
- PASS: Boundary fixture: start/end dates, duplicate lines, customer without orders, order without lines
- PASS: All three late-order rewrites agree
- PASS: Aggregate WHERE fails; HAVING succeeds

Fixture expected result: X / 1 customer / 60.00 revenue. The order without lines is excluded by INNER JOIN; a city without qualifying lines is absent.

Invalid aggregate WHERE error: `misuse of aggregate: COUNT()`.
