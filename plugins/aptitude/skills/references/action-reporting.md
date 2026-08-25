# Aptitude Action Reporting

Use this reference for every user-facing result from an Aptitude MCP action.
Keep reports limited to the action, target, result, inspection, scores,
warnings, changes, and a safe next step. Do not copy credentials, tokens,
internal plans, or unrelated response fields.
Do not report telemetry.

Canonical maturity, security, and overall scores are displayed out of 10;
machine-normalized values in the range [0,1] are reported for machine
consumers. Performance evidence is non-persisted and must be labeled as such
when present. Do not report trust or trust_tier labels or fields in skill action
reports. Resolver
preference or policy reports may include `allowed_trust_tiers` only as the
configured policy field.

Use the canonical fields `maturity_score`, `security_score`, and
`overall_score`; human-readable results render them as `/10`, while machine
formats retain their normalized values.

Format a skill coordinate as `slug-name@vx.y.z`. Use a standalone version in
backticks, such as `v0.1.0`.

## Publisher actions

- `aptitude_publisher_inspect_skill`: report the local skill path, evaluated
  coordinate and intent, inspection result, validation and gate result, scores,
  non-persisted performance evidence when present, warnings, and receipt
  freshness or reuse metadata. Inspection is local and does not upload anything
  to the registry.
- `aptitude_publisher_publish_skill`: report the confirmed coordinate, the
  registry target, the publish result, and the resulting registry location or
  failure. Publish only after the existing explicit confirmation gate.

## Resolver actions

- `aptitude_search_skills`: report the search target and the returned candidate
  summary, including the selected candidate when one is chosen.
- `aptitude_inspect_skill`: report the inspected coordinate and the
  user-relevant metadata, validation, and warnings.
- `aptitude_resolve_skill`: report the selected coordinate and the
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
**Action: <inspect-for-publish|inspect-for-install|publish|install|policy update>**
- Target: <skill, path, scope, registry, or configuration layer>
- Result: <concise user-visible outcome, including status when useful>
- Inspection: <inspection status with validation and gate result; Publisher only>
- Scores: <named canonical scores, or not scored; inspection actions when available>
- Reason: <exact tool-provided reason; blocked or failed only>
- Warnings: <relevant warnings; omit when none>
- Changes: <changed files, registry state, or none>
- Next: <safe follow-up; omit when none>
```
