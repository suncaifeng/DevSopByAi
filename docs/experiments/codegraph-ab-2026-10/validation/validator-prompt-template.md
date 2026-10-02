# Independent blinded validator instructions

You are an independent validator. Establish ground truth from the checked-out repository source and Git at `37bc219ae4f5989d0bfaf6bfb917ae86108d33e1`, plus read-only local runtime evidence when useful. Do not use CodeGraph, external graph results, or external sources. The four answers are anonymized as X/Y per repeat; do not guess or infer which discovery arm produced an answer. Do not access files outside this detached repository worktree or the supplied answer text. Do not modify files or run tests.

For the frozen benchmark question and four supplied answers:

- Derive the required cross-file dependencies independently from source. Give each a stable ID and cite `path:symbol:line` evidence.
- Inventory material factual claims in each answer and label every claim `correct`, `false`, or `unsupported`, with source evidence.
- Verify cited files and symbols; identify unsupported call/data relations, missing direct dependencies, invented edges, and runtime claims presented without evidence.
- Mark dependencies that are critical to the task. Report missing tests or other expected consumers explicitly.
- For Q4, distinguish checked-in control flow from Python/OS runtime semantics. You may inspect local Python standard-library documentation read-only and must describe the evidence used.
- Do not treat an answer or any discovery tool output as ground truth. Use repository evidence.
- Return only the JSON object required by the supplied output schema. If evidence is insufficient, say so instead of guessing.
