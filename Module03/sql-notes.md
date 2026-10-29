# Module 03 — SQL Notes and Verification

Prepared and verified locally on my Windows computer. I ran the benchmark and injection demonstration, inspected query plans, and discussed the module with İsa.

## References

- [Course module](https://github.com/iotempire/iotempire-teaching/blob/main/full-classes/hsbi-databases-10d/modules/03-llm-assisted-sql-and-query-profiling.md)
- [Dataset setup](setup.sql)
- [Dashboard query](queries.sql)
- [Benchmark and query plans](benchmark.md)
- [Plan safari and optional rewrites](extra-plans.md)

Further reading:

- [SQLite query plans](https://www.sqlite.org/eqp.html)
- [Python sqlite3 and parameter binding](https://docs.python.org/3/library/sqlite3.html)
- [OWASP SQL injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

## Materials consulted

The preparation used the course instructions, feedback-round manual, reflection template and existing Module02 setup.  The reference links above provide further reading.

## Task prompt and AI assistance

The following prompt comes from the course instructions and was used as the query specification:

> SQLite schema: customer(customer_id, name, city), product(product_id, sku, price), orders(order_id, customer_id, ordered_on, status), order_line(order_id, product_id, qty). Write a query that returns, for each city, the number of distinct customers and the total revenue (sum of qty*price) of orders placed in 2025, ordered by revenue descending.

The SQL in [queries.sql](queries.sql) was prepared with AI assistance and follows the course reference query. The optimization suggestions and AI-provided predictions recorded before the initial execution are in [predictions.md](predictions.md). These are not independent student predictions.

The grouped late-orders query was the default approach. Correlated-subquery and window-function alternatives are recorded in [extra-plans.md](extra-plans.md).

## Local execution and correctness checks

I ran:

```powershell
python Module03/bench.py
python Module03/injection_demo.py
```

The database contained:

| Table | Rows |
|---|---:|
| customer | 2,000 |
| product | 500 |
| orders | 60,000 |
| order_line | 240,000 |

The benchmark completed these checks successfully:

- Expected row counts.
- Identical query results across index configurations.
- Dashboard results matching a separate Python calculation from the base tables.
- Correct handling of date boundaries and repeated order lines.
- Matching results from grouped, correlated-subquery and window-function reports.
- An aggregate condition failing in WHERE and succeeding in HAVING.

The small verification dataset includes the start of 2025, the end of 2025, dates outside the year, repeated customers, a customer without orders and an order without lines.

### What the dashboard actually counts

`COUNT(DISTINCT c.customer_id)` counts each customer once per city, even when joins produce several rows for that customer.

The INNER JOINs include only customers with qualifying order lines. Customers without orders and orders without lines are excluded. Cities without qualifying lines are omitted rather than displayed with zero revenue.

If the requirement includes all registered customers or all cities, the query needs a different join and aggregation strategy.

## Benchmark method

[benchmark.md](benchmark.md) contains the query plans and timing table. [results.json](results.json) contains the raw samples and environment details.

The script:

- Captures EXPLAIN QUERY PLAN before timing.
- Uses the same database connection.
- Performs a warm-up before each measurement.
- Reports the median of three samples.
- Batches short queries 30 times per sample.
- Fetches all result rows.
- Tests indexes individually and in combinations.
- Does not run ANALYZE.

The timings include Python overhead and reflect this dataset and execution environment. They can vary between runs.

## Main findings

### A selective lookup benefits from an index

For the single-day query, the date index changed the order-table access from a scan to:

```text
SEARCH o USING INDEX ix_orders_ordered_on (ordered_on=?)
```

The local measurements showed a substantial reduction in execution time.

### More indexes do not guarantee a faster report

The annual dashboard became slower when the date and order-line indexes were combined.

A broad date range still processes many rows. Repeated index and table lookups can cost more than scanning the order lines. This is a possible explanation consistent with the changed plan and measured times.

A SEARCH is not automatically better than a SCAN.

### A timing change alone is not proof

In the initial recorded experiment, the date index alone left the dashboard plan unchanged. A timing difference without a plan change does not establish that the index improved execution; cache effects and system load can also affect the result.

The current local plans are preserved in benchmark.md for comparison.

### An index is useful for particular queries

The product index was not used by the dashboard in the initial experiment, but it was used for a direct filter on `order_line.product_id`.

Therefore, “not useful for this query” is more precise than “useless index.”

### Wrapping a column in a function can prevent an index search

The local plan for the wrapped-date query showed:

```text
SCAN o
```

Using `date(ordered_on)` prevented a search through the ordinary index on `ordered_on`. An appropriate expression index would be a different case.

## Query-plan vocabulary

| Term | Meaning |
|---|---|
| SCAN | Walk through a table or index rather than narrow the read to an indexed range. |
| SEARCH | Use a key or index condition to narrow the read. |
| COVERING INDEX | Obtain all required values from the index without fetching the table row. |
| USE TEMP B-TREE | Use a temporary structure for sorting, grouping or distinct values. |

A scan can be reasonable when a query needs a large proportion of the data.

The covering-index examples in [extra-plans.md](extra-plans.md) compare selecting only an indexed column with selecting an additional column from the table.

The safari also demonstrates that a column named `machine_name` is not automatically a primary key. Without a suitable index, an equality condition can still require a scan.

## SQL clause order

Written order:

`SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY`

Logical order:

`FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`

A tested example:

```sql
-- Invalid: aggregate conditions cannot be evaluated in WHERE.
SELECT city, COUNT(*) AS n
FROM customer
WHERE COUNT(*) > 1
GROUP BY city;

-- Valid: HAVING filters groups after aggregation.
SELECT city, COUNT(*) AS n
FROM customer
GROUP BY city
HAVING COUNT(*) > 1;
```

Both cases are checked by bench.py.

SQLite allows some nonstandard uses of aliases, so a SELECT alias in WHERE is not a reliable example of an error in every case. Logical clause order also does not determine the physical join order chosen by the optimizer.

## Relational algebra and SQL

### Simple selection

```sql
SELECT *
FROM maint_job
WHERE technician = 'Beier';
```

Relational-algebra expression:

`σ technician='Beier' (maint_job)`

Selection keeps the matching rows. SELECT * retains all columns, so a separate projection is unnecessary.

This expression was prepared with AI assistance. My independent expression and comparison are still pending.

### Dashboard expression

Using extended relational algebra with SQL bag semantics:

1. Join the four tables:

   `J = (customer ⋈ customer.customer_id=orders.customer_id orders) ⋈ orders.order_id=order_line.order_id order_line ⋈ order_line.product_id=product.product_id product`

2. Select orders from 2025:

   `F = σ ordered_on>='2025-01-01' AND ordered_on<'2026-01-01' (J)`

3. Group by city and calculate the aggregates:

   `G = γ city; COUNT_DISTINCT(customer_id)→customers, SUM(qty*price)→revenue (F)`

4. Select the output columns:

   `π city,customers,revenue (G)`

5. Sort by revenue descending using the ordering extension:

   `τ revenue DESC`

Selection corresponds to WHERE, joins to JOIN ON, grouping to GROUP BY, and projection to the SELECT list.

Classical relational algebra uses sets, whereas SQL normally preserves duplicate rows. This distinction matters for repeated order lines and SUM. Sorting is an extension rather than part of classical relational algebra.

## SQL injection and bound parameters

The local demonstration produced:

```text
normal: [(1, 'Customer 1')]
apostrophe crash: near "Brien": syntax error
payload: ' OR '1'='1
unsafe payload: 2000 rows
safe payload: []
safe apostrophe: [(2001, "O'Brien")]
```

String interpolation mixes user input with SQL syntax. The injection payload changes the condition and returns every customer. A normal name such as O'Brien also breaks the vulnerable query because of its apostrophe.

The safe version uses:

```python
sql = "SELECT customer_id, name FROM customer WHERE name = ?"
conn.execute(sql, (name,))
```

The placeholder keeps the value separate from the SQL structure. The payload is treated as a literal name and returns no matches, while O'Brien works correctly.

The temporary customer used to test the apostrophe is rolled back afterwards.

### Why not remove or escape quotes manually?

Removing quotes damages valid names and does not solve every SQL construction problem. Manual escaping depends on the context and is easy to implement incorrectly.

Use bound parameters for values. Placeholders do not replace table or column identifiers; dynamic identifiers need a fixed allow-list. Parameterization does not replace access control.

## Setup curiosities

| Source | Question | Explanation |
|---|---|---|
| [setup.sql](setup.sql), recursive CTEs | Where do the generated rows come from? | Start with 1 and repeatedly add 1 until the limit. INSERT consumes those rows. |
| setup.sql, INSERT SELECT | What happens if SELECT returns no rows? | No rows are inserted. This is a reasoning note rather than a separate recorded experiment. |
| setup.sql, modulo expression | Why do customer references fit? | `(x % 2000) + 1` generates values from 1 to 2,000, matching the generated customers. No foreign key enforces this yet. |
| setup.sql, date expression | What happens when x = 540? | The remainder is zero, producing 2025-01-01. Concatenation builds the date modifier string. |
| setup.sql, printf | What does `%05d` mean? | Format an integer with at least five digits, adding leading zeros, such as SKU-00001. |
| setup.sql, repeated modulo | Is the dataset realistic? | It is deterministic test data. Each order has four repeated product lines, and customer and status values are correlated. |
| [benchmark.md](benchmark.md) | Why can indexed lookups be slower? | A broad query may perform many lookups. Compare its plan and measurements with the scan. |
| [extra-plans.md](extra-plans.md) | Why does the window version use DISTINCT? | The window count appears on every matching order row; DISTINCT reduces the output to one row per customer. |

## Peer discussion and next steps

I discussed the module with İsa. We both found organizing the work and locating small mistakes challenging. This was a general discussion rather than a detailed comparison of our query plans.

Still to complete:

- My independent relational-algebra attempt and comparison.
- A comparison of SQLite versions and plans with another pod.
- The curiosity swaps and feedback notes.
- Recording any questions actually posted to #sql-questions.

A question to discuss:

> Why can SQLite choose an indexed plan for the annual report when the measured scan is faster?

My personal learning experience is recorded in [Reflection 03](../Reflections/ref03.md).