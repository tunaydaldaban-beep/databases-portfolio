# Reflection 02 — Data contracts and legacy schemas

**PENDING — TUNAY TO REVIEW AND COMPLETE IN HIS OWN WORDS**

This is a technical preparation draft based on actual assistant execution. It does not claim that Tunay has performed the checks or experienced the observations below.

## Take-away

Technical observation to consider: a table can store data successfully while failing to express relationships. The maintenance fixture contains an orphan, duplicate part records and a comma-separated relationship. Tunay: explain how this changed your understanding, if it did.

## What was good?

The fixture, SQL audit and contract form a reproducible workflow. All 25 contract tests passed in isolated databases. Tunay: describe what worked when you tried it yourself.

## What was difficult?

The naive join loses the multi-part job and duplicates another job. SQLite affinity and optional participation need more care than a diagram suggests. Tunay: add the part you actually found difficult and how you addressed it.

## Exploration and show stoppers

The proposed five-table model separates technician identity and normalizes job parts. Data migration is deliberately deferred because the orphan and unknown date need real decisions. Tunay: add your own questions, experiments and unresolved problems.

## Interaction with peers and instructors

PENDING: actual Module 2 study/pod discussion, neighboring-pod feedback and any instructor interaction. Do not copy the Module 1 meeting as evidence for this activity.

## How did you verify AI suggestions?

The assistant executed the SQL against the original fixture, rebuilt the corrected DDL and ran 25 validation/constraint tests. Results are linked in [Module 2](../Module02/README.md). Tunay: identify which checks you personally reran, what you inspected, and what you can explain from the output.

## Help and extra work

ChatGPT prepared the technical implementation and this draft from the workbook and supplied master prompt. Tunay: describe your actual review, changes and any additional sources used. Optional exercises and remaining work are recorded in the [completion report](../Module02/technical-completion-report.md).
