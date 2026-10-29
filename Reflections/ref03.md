# Reflection 03 — LLM-Assisted SQL and Query Profiling

## Take-away

This module helped me see how databases can support industrial applications, such as tracking orders and preparing reports. Working with related tables and SQL queries gave me a better understanding of some of the backend work behind a user interface. I also learned that adding an index does not automatically make every query faster.

## What was good?

Running the examples on my own computer made the concepts more concrete. I could compare query timings and see where SQLite used an index. The SQL injection example also clearly showed the difference between building a query with strings and using bound parameters.

## What was difficult?

Finding the cause of an error was sometimes harder than running the code itself. A small mistake, such as an incorrect quotation mark, could stop the script. Organizing the files and understanding how the different parts worked together also required attention.

## Exploration and show stoppers

The benchmark showed that an index could speed up a single-day lookup while a combination of indexes made the annual report slower. This helped me understand why measurements and query plans should be checked together. I still need more practice explaining why the database chooses a particular plan.

## Interaction with peers and instructors

I discussed the module with my groupmate, İsa Babayev. We had similar difficulties with organizing the work and identifying mistakes in the code. Comparing our experiences showed that these challenges were shared, although we have not yet recorded a detailed comparison of our query plans.

## How did you verify AI suggestions?

AI supported the preparation of the scripts and explanations, and I consulted it when parts were difficult or errors occurred. I ran the benchmark and injection demonstration on my own Windows computer. The checks compared SQL results with a separate Python calculation and tested date boundaries. I also inspected the query plans to identify index searches and table scans.

## Help and extra work

Discussing difficulties with İsa and using AI explanations helped me work through the module. The optional subquery and window-function examples were also included in the scripts I ran, and their results matched. My next step is to practise explaining the queries and results more independently.