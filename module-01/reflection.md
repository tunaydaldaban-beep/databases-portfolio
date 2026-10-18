# Reflection — review and personalize before submission

This is an AI-assisted technical draft, not a claim about the student's personal experience.

## What worked?
The prepared generator creates reproducible telemetry. The Python loader uses parameter binding. The analysis compares SQL results with an independent CSV calculation. See the recorded evidence.

## What broke?
A deliberately incorrect LIKE '%18%' filter matched a date containing 18, not just the time. The phrase “overnight” also needs a precise start/end definition. **[Add your own installation or coding difficulties.]**

## How did my mental model shift?
**[Personalize:]** A database can be a library used directly by a program; a separate database service is not required for this local exercise. Whether a server is useful depends on the workload and access requirements.

## How did I verify AI suggestions?
The provided checks execute the SQL, inspect EXPLAIN QUERY PLAN, compare against CSV calculations and test time boundaries. **[Describe the checks you personally reran and understood.]**
