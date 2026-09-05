---
name: inspect-for-install
description: Use when evaluating a registry Aptitude skill before deciding whether to install it.
---

# Inspect a Registry Skill for Installation

Use this non-mutating discovery workflow when a user wants to find a registry
skill to install:

1. Scan the target project for relevant evidence before searching. Reuse current
   evidence when available. Inspect manifests (`pyproject.toml`, `package.json`),
   lockfiles (`uv.lock`, `poetry.lock`, `bun.lock`, `pnpm-lock.yaml`), tool
   configuration, test directories, and existing agent skills. Read relevant
   sections only; skip secrets, dependency caches, and generated files. In a
   monorepo, use the requested package; do not infer its ecosystem from unrelated
   sibling packages. If evidence is absent or mixed, state the uncertainty.
2. Search with `aptitude_search_skills`, combining the user's task with evidenced
   ecosystem and tools. Send concise search terms, not project file contents.
   For a broad request, compare 2–3 relevant returned candidates when available;
   do not invent alternatives or replace an explicitly requested skill.
3. Inspect promising candidates with `aptitude_inspect_skill` when search
   results do not provide enough detail.
4. Briefly explain the project evidence behind the recommendation, for example:
   “Your `pyproject.toml` lists pytest and you have `uv.lock`, so I searched for
   Python testing skills.” Only make that claim when those files support it.
   Show what each candidate has to offer: coordinate, purpose, fit for the
   request, maturity/security/overall scores displayed out of 10, dependencies,
   and warnings. Mention useful bundled scripts, references, examples, or assets
   when inspection confirms them; do not execute them during discovery.
   Distinguish related candidates: `pytest` offers tool-specific guidance while
   `python-testing` covers broader testing practices. If returned metadata shows
   that pytest depends on python-testing, explain that selecting pytest also
   brings in python-testing. Recommend one with an evidence-based reason.
5. Ask one combined question headed "Which one to install?" that collects the
   selected candidate, target agents, and project/global/custom scope. Include
   the custom path in that same question when `scope: "custom"` is relevant.
6. After the user selects, inspect the selected coordinate with
   `aptitude_inspect_skill` and resolve it with `aptitude_resolve_skill`. Report
   the exact policy outcome, direct and transitive dependencies (shared skills
   listed once), warnings, and selected destination inputs without installing.

This workflow does not install skill/project files and does not mutate the registry;
advisory cache updates may occur in the resolver. Do not resolve or install
before the user selects a candidate and destination inputs. Do not ask
separate agent, scope, path, or approval questions.

Keep the comparison limited to decision-useful inspection information; do not
copy credentials, internal plans, or unrelated fields.

Use the [shared action-reporting reference](../references/action-reporting.md)
for the concise result. After successful resolution, the safe next step is the
separate installation workflow, which previews the exact plan before one approval.
