---
name: install-skill
description: Use when a user requests installing an Aptitude registry skill into named agents and scope, or when a reviewed registry inspection is ready for installation.
---

# Install Aptitude Skill

This is the mutation workflow. If no reviewed inspection exists for the same
coordinate, use [inspect-for-install](../inspect-for-install/SKILL.md) first.
Do not duplicate the inspection workflow or install by a guessed name.

Use the Aptitude MCP. Do not use local resolver commands.
Use the [shared action-reporting reference](../references/action-reporting.md) for the user-facing result.

1. Require the explicit selected coordinate, target agents, and scope.
2. Call `aptitude_preview_install_destinations` for those same agents and scope.
3. State the coordinate, agents, scope, destinations, and warnings. Get explicit confirmation
   before calling `aptitude_install_skill` with those same targets. No fresh unpinned resolution
   is allowed after confirmation.

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

If the user has not supplied agents or scope, ask; never choose defaults for a
write. Report MCP errors without weakening policy or retrying with different
targets.
