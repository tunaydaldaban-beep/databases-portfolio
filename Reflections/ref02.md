# Reflection 02 — Data Contracts and Legacy Schemas

## Take-away
This module helped me better understand how software follows instructions and how databases organize information. It felt a little like teaching someone who knows nothing about the task: we need to explain clearly what is allowed and how things are connected. A database cannot guess our intentions, so the rules we define matter.

## What was good?
I ran the audit and tests on my own Windows computer. All 25 tests passed, and the additional inheritance checks also completed successfully. Seeing concrete examples made the connection between the code, the stored data and the rules easier to understand.

## What was difficult?
The hardest part was translating what I wanted into precise instructions. A rule can sound obvious in everyday language but still need several constraints in the database. Understanding how primary keys, foreign keys and validation work together required careful attention.

## Exploration and show stoppers
One important lesson from the examples is that a query can run successfully and still produce an incomplete or misleading result. The parts query showed this by leaving out a maintenance job and returning another one twice. This demonstrates why checking the output matters as much as checking whether the code runs.

## Interaction with peers and instructors
I discussed the module with my groupmate, İsa Babayev. We talked about our general understanding and had similar impressions about the difficulty of expressing instructions clearly. Our conversation was brief, and we did not carry out a detailed review of each other's queries or diagrams.

## How did you verify AI suggestions?
I used ChatGPT to help prepare the scripts, diagrams and explanations. I then ran the audit and automated tests locally. These checked examples such as duplicate records, missing references and invalid prices. The successful results provided evidence that the tested rules worked, although passing tests alone does not prove that every possible situation is covered.

## Help and extra work
ChatGPT helped with the organizing my comments into this reflection. I also ran the optional EER inheritance examples, which compared a single-table design with separate subtype tables.