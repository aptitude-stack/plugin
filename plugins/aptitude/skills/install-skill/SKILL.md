---
name: install-skill
description: Use when a user requests installing an Aptitude registry skill into named agents and scope, or when a reviewed registry inspection is ready for installation.
---

# Install Aptitude Skill

This is the preview and mutation workflow. If no candidate and destination were
selected together, use [inspect-for-install](../inspect-for-install/SKILL.md)
first. Do not install by a guessed name.

Use the Aptitude MCP. Do not use local resolver commands.
Use the [shared action-reporting reference](../references/action-reporting.md) for the user-facing result.

After the user selects the candidate, target agents, and scope in one combined
answer and the inspection workflow resolves that selection:

1. Stop on a failed or stale policy result; do not install.
2. Call `aptitude_preview_install_destinations` with the exact reviewed agents and
   scope.
3. Preview the exact reviewed coordinate, resolved dependencies, agents, scope,
   destination paths, changes, and warnings. Ask for one explicit confirmation
   (one approval) of that full installation plan.
4. After approval, call `aptitude_install_skill` with those exact reviewed
   inputs. No fresh unpinned resolution or destination change is allowed.

Call `aptitude_install_skill` with the exact reviewed query and coordinate, plus
the same destination inputs used for the preview:

```json
{
  "query": "<reviewed-query>",
  "select_slug": "<reviewed-slug>",
  "version": "<reviewed-version>",
  "agents": ["<preview-agent>"],
  "scope": "<preview-scope>",
  "cwd": "<preview-cwd>",
  "export_root": null
}
```

For `scope: "custom"`, replace `null` with the same explicit `export_root`
used in the destination preview. Do not change the query, slug, version,
agents, scope, cwd, or export root between preview and install.

If required destination inputs are missing, ask one combined follow-up for all
of them before previewing; never choose write defaults. Report MCP errors
without weakening policy or retrying with different targets.
