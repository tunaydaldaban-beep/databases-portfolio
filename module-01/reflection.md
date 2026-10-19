# Reflection

## What worked?

I successfully generated the telemetry CSV, loaded 172,800 rows into SQLite and ran the analysis script. The checks passed, and I saved the outputs in my portfolio. Using SQL together with Python gave me more practical experience.

## What broke?

At first, PowerShell did not recognize uv or sqlite3. After installation and restarting the terminal, both worked. I also had problems with the location of the module-01 folder, which caused a file path error.

The analysis included an intentionally incorrect LIKE '%18%' filter. This showed why matching text in a timestamp is not the same as filtering by time. The meaning of "overnight" also needed a clear time range.

## How did my mental model shift?

I started to see databases as a way to organize information clearly. Tables and columns give the data a structure, and SQL helps select and filter what is needed. This made databases feel less complicated than they looked from the outside.

I already knew a little about SQL and using databases with Python, but this exercise made those connections more practical.


## How did I verify AI suggestions?

I ran the generator, loader, analysis script and SQLite shell tour on my own computer. I reviewed all the checks and worked through the results to understand them, including the comparison between SQL results and independent CSV calculations and the time-boundary tests. When something was unclear, I used ChatGPT to help explain it.

## AI assistance

I used ChatGPT for support where I needed help. I ran the commands myself and reviewed their outputs. The personal observations in this reflection are my own, with AI assistance used to express them in English.