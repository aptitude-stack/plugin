---
name: inspect-for-install
description: Use when evaluating a registry Aptitude skill before deciding whether to install it.
---

# Inspect a Registry Skill for Installation

Use this non-mutating evaluation workflow when a user wants to evaluate a
registry skill before installation. Search, inspect, and resolve as needed:

1. Search with `aptitude_search_skills`.
2. Inspect candidates with `aptitude_inspect_skill`.
3. Resolve the selected coordinate with `aptitude_resolve_skill`.

This workflow does not install skill/project files and does not mutate the registry;
advisory cache updates may occur in the resolver. Stop before any destination
preview or mutation.

Report the selected coordinate, relevant canonical maturity, security, and
overall scores displayed out of 10, warnings, the exact policy outcome, and a
safe next step. Keep the report limited to user-relevant inspection and policy
information; do not copy credentials, internal plans, or unrelated fields.

Use the [shared action-reporting reference](../references/action-reporting.md)
for the concise result. Installation requires the separate mutation workflow
and an explicit target choice.
