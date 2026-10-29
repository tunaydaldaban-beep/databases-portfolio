# Reflection 01 — Introduction and Local-First Foundations

## Take-away

This module helped me understand how databases organize information through tables and columns, and how SQL selects and filters the data we need. I already knew a little about SQL and Python, but working with them together made the connection more practical.

My main advice to myself is to check what a query actually means, not only whether it runs without an error.

## What was good?

I generated the telemetry CSV, loaded 172,800 rows into SQLite and ran the analysis on my own computer. The checks passed, and I saved the outputs in my portfolio. Seeing the complete process from data generation to query results helped me understand the workflow.

## What was difficult?

At first, PowerShell did not recognize uv or sqlite3. Installing the tools and restarting the terminal resolved this. I also had a file path problem because of the location of the module-01 folder.

These problems showed me that organizing files and checking the working directory are important parts of running code.

## Exploration and show stoppers

An intentionally incorrect LIKE '%18%' filter showed why searching for text inside a timestamp is different from filtering by time.

The word "overnight" also needed clarification. A query for readings after 18:00 does not include the early morning hours. The intended time range should be confirmed before treating the query as correct.

## Interaction with peers and instructors

The peer feedback on my Module 1 work raised the question of whether the overnight query should include the early morning until 06:00. This was useful because it focused on the meaning of the query rather than only its syntax.

I also reviewed İsa's Module 1 work and prepared feedback on his SQL and verification approach.

## How did you verify AI suggestions?

I ran the data generator, loader, analysis script and SQLite shell tour locally. The verification compared SQL results with separate calculations from the CSV and checked time boundaries.

I reviewed the outputs and used AI explanations when something was unclear. A successful execution alone was not enough; the results also needed to match the intended question.

## Help and extra work

AI provided some support with the technical work and explanations. I ran the commands myself and reviewed their outputs.

The peer review was also valuable because it highlighted an assumption that needed clarification. My next step is to become more confident explaining the queries and their limitations independently.