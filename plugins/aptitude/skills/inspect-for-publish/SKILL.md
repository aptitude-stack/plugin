---
name: inspect-for-publish
description: Use when checking a local Aptitude skill before a possible registry publication.
---

# Inspect a Local Skill for Publishing

Use this workflow only for local pre-publication inspection. It does not upload
and does not mutate the registry; it does not publish a skill.

The Publisher writes local `.publisher_artifacts/` and an inspection receipt;
that local evidence makes no upload or Registry mutation.

Call `aptitude_publisher_inspect_skill` with the local folder:

```json
{"skill_path": "<local-skill-path>"}
```

Report the evaluated path, coordinate, and intent; validation and gates;
canonical maturity, security, and overall scores displayed out of 10; any
performance evidence clearly marked non-persisted; warnings; and receipt
freshness, reuse, or refresh metadata. Stop and report the exact reason when
inspection is blocked. Do not treat local performance evidence as a persisted
registry metric.

Use the [shared action-reporting reference](../references/action-reporting.md)
for the concise result. Keep credentials, internal plans, and unrelated tool
fields out of the report. This inspection does not authorize publication.
