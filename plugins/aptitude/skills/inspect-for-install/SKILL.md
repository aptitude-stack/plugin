---
name: inspect-for-install
description: Use when evaluating a registry Aptitude skill before deciding whether to install it.
---

# Inspect a Registry Skill for Installation

Use this non-mutating discovery workflow when a user wants to find a registry
skill to install:

1. Search with `aptitude_search_skills`.
2. Inspect promising candidates with `aptitude_inspect_skill` when search
   results do not provide enough detail.
3. Show what each candidate has to offer: coordinate, purpose, fit for the
   request, maturity/security/overall scores displayed out of 10, dependencies,
   and warnings.
4. Ask one combined question headed "Which one to install?" that collects the
   selected candidate, target agents, and project/global/custom scope. Include
   the custom path in that same question when `scope: "custom"` is relevant.
5. After the user selects, inspect the selected coordinate with
   `aptitude_inspect_skill` and resolve it with `aptitude_resolve_skill`. Report
   the exact policy outcome, dependencies, warnings, and selected destination
   inputs without installing.

This workflow does not install skill/project files and does not mutate the registry;
advisory cache updates may occur in the resolver. Do not resolve or install
before the user selects a candidate and destination inputs. Do not ask
separate agent, scope, path, or approval questions.

Keep the comparison limited to decision-useful inspection information; do not
copy credentials, internal plans, or unrelated fields.

Use the [shared action-reporting reference](../references/action-reporting.md)
for the concise result. After successful resolution, the safe next step is the
separate installation workflow, which previews the exact plan before one approval.
