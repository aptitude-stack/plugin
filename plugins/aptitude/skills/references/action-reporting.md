# Aptitude Action Reporting

Use this reference for every user-facing result from an Aptitude MCP action.
Keep reports limited to the action, target, result, warnings, changes, and a
safe next step. Do not copy credentials, tokens, internal plans, or unrelated
response fields.
Do not report telemetry.

## Publisher actions

- `aptitude_publisher_inspect_skill`: report the local skill path, evaluated
  slug/version/intent, validation and gate result, warnings, and whether local `.publisher_artifacts/`
  were written. Inspection is local and does not upload anything to the registry.
- `aptitude_publisher_publish_skill`: report the confirmed slug/version, the
  registry target, the publish result, and the resulting registry location or
  failure. Keep the local inspection artifacts distinct from the registry
  change. Publish only after the existing explicit confirmation gate.

## Resolver actions

- `aptitude_search_skills`: report the search target and the returned candidate
  summary, including the selected candidate when one is chosen.
- `aptitude_inspect_skill`: report the inspected skill/version and the
  user-relevant metadata, validation, and warnings.
- `aptitude_resolve_skill`: report the selected coordinate/version and the
  policy outcome. Summarize the result without reproducing internal planning
  details or unrelated fields.
- `aptitude_preview_install_destinations`: report the requested agents and
  scope, the resolved destinations, and any destination warnings or blockers.
- `aptitude_install_skill`: report the confirmed agents and scope, the
  installation result, and the files or destinations changed. If blocked,
  state that no installation was made.

## Resolver preference actions

- Initial read with `aptitude_show_policy`: report effective selection, each
  selection field's source, effective policy, aggregate policy source, and
  contributing layers.
- Edit: after explicit confirmation, report the requested user or workspace
  layer, the values written, and preserved unrelated fields. State if a
  restrictive layer prevents the requested layer from winning.
- Post-read with `aptitude_show_policy`: use the same `cwd` and JSON response
  format, then report effective selection and each field's source, effective
  policy and aggregate source, contributing layers, and which layer won.

### Report format

```markdown
- Action: <inspection|publish|install|policy update>
- Target: <skill, path, scope, registry, or configuration layer>
- Result: <concise user-visible outcome, including status when useful>
- Reason: <exact tool-provided reason; blocked or failed only>
- Warnings: <relevant warnings; omit when none>
- Changes: <changed files, registry state, or none>
- Next: <safe follow-up; omit when none>
```
