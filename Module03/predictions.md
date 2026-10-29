# Predictions recorded before execution

Prepared by ChatGPT during the assisted work, not claimed as Tunay's independent predictions.

Dashboard: expect SCAN ol, primary-key SEARCH on orders/customer/product, temporary B-trees for grouping, DISTINCT counting and ordering. A broad annual range may not benefit from the date index. An order-line index may change join order without improving time.

Single day: expect SCAN o without an index and SEARCH o USING INDEX ix_orders_ordered_on with it. Wrapping ordered_on in date() should prevent a search using this ordinary index.

Safari: all three queries should initially SCAN because the legacy schema has no keys or indexes. Adding ix_job_tech should change only technician equality to SEARCH. Leading-wildcard LIKE and lower(technician) should still SCAN.

Optimization proposal: test indexes on orders(ordered_on), order_line(order_id), and order_line(product_id), both independently and cumulatively. Keep only claims supported by the measured plans; do not assume every index helps.
