---
name: inspect-for-publish
description: Use when checking a local Aptitude skill before a possible registry publication.
---

# Inspect a Local Skill for Publishing

Use this workflow for local publication discovery and inspection. It does not upload,
does not mutate the registry, and does not publish a skill.

1. Within the user-named path or workspace, discover plausible local skill
   directories containing `SKILL.md`. Do not inspect secret files.
2. Show what each candidate has to offer: path, frontmatter purpose, and any
   available slug, version, and intent. Do not invent missing identity fields.
3. Ask one combined question headed "Which one to publish?" that collects the
   selected local path and registry target.
4. After selection, call `aptitude_publisher_inspect_skill` with that path and
   use its result as the non-mutating publication preview.

The Publisher writes local `.publisher_artifacts/` and an inspection receipt;
that local evidence makes no upload or Registry mutation.

Call the inspection with the selected local folder:

```json
{"skill_path": "<local-skill-path>"}
```

Preview the evaluated path, coordinate, intent, and registry target; validation and gates;
canonical maturity, security, and overall scores displayed out of 10; any
performance evidence clearly marked non-persisted; warnings; and receipt
freshness, reuse, or refresh metadata. Stop and report the exact reason when
inspection is blocked. Do not treat local performance evidence as a persisted
registry metric.

Use the [shared action-reporting reference](../references/action-reporting.md)
for the concise result. Keep credentials, internal plans, and unrelated tool
fields out of the report. This inspection does not authorize publication; the
complete preview receives one approval in the publication workflow.
