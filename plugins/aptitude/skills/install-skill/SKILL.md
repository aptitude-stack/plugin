---
name: install-skill
description: Use when finding, evaluating, or installing an Aptitude skill into an explicit agent and scope.
---

# Install Aptitude Skill

Use the Aptitude MCP. Do not use local resolver commands or install by a guessed name.
Use the [shared action-reporting reference](../references/action-reporting.md) for the user-facing result.

1. Search with `aptitude_search_skills`, then inspect promising candidates with
   `aptitude_inspect_skill`.
2. Resolve the selected candidate with `aptitude_resolve_skill` and review its
   selected coordinate, policy, lockfile, and execution plan.
3. Call `aptitude_preview_install_destinations` for the requested agents and scope.
4. State the resolved skill/version, agents, scope, and destination. Get explicit confirmation
   before calling `aptitude_install_skill` with those same explicit agents and scope.

If the user has not supplied agents or scope, ask; never choose defaults for a
write. Report MCP errors without weakening policy or retrying an install with
different targets.
