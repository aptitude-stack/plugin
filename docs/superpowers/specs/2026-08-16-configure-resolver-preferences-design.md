# Configure Resolver Preferences Skill

## Scope

Add one Aptitude plugin skill at `plugins/aptitude/skills/configure-resolver-preferences/SKILL.md`.
It configures the resolver's existing local selection preferences and restrictive
policy. It does not add a publisher configuration skill: publisher settings are
per-run metadata or evaluator/transport controls, not personalized policy.

## Workflow

1. Inspect the effective configuration with `aptitude_show_policy`.
2. Ask whether the requested setting belongs in user or workspace scope, and
   obtain confirmation before editing the selected `aptitude.toml`.
3. Keep `[selection]` separate from `[policy]`:
   selection is soft ranking/prompt behavior; policy constrains legal skills.
4. Preserve unrelated TOML fields and never silently broaden an active policy.
5. Re-run `aptitude_show_policy` and report effective values plus their sources.

## Supported Settings

- `[selection]`: `profile`, `interaction_mode`, `candidate_limit`.
- `[policy]`: allowed trust tiers, allowed lifecycle statuses, per-skill and
  whole-graph token/content-size ceilings.

The skill excludes `[execution]` concurrency because it is operational tuning,
not personalization.

## Verification

Add a focused plugin test that asserts discovery-critical instructions:
policy inspection, scope selection, the soft-versus-hard distinction, explicit
confirmation before writes, preservation/no silent relaxation, and post-edit
verification. Validate the plugin test suite after the skill is written.
