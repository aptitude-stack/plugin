---
name: prepare-aptitude-skill
description: Use when adapting an existing agent skill that lacks Aptitude metadata or needs local Aptitude compatibility checks.
---

# Prepare an Aptitude Skill

Create a reviewable converted draft. Do not publish or run Aptitude Publisher.

## Instructions

1. If the source path is missing or ambiguous, stop and report the blocker.
   Otherwise resolve the exact skill root and inspect `SKILL.md` plus non-secret
   supporting files. Do not read dotenv files, credentials, caches, Publisher
   artifacts, or an existing `draft/`.
2. Record the source file inventory and content checksums. Copy the useful skill
   package into `<skill-root>/draft/`; keep the source unchanged. Preserve useful `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`.
3. Normalize the draft:
   - Keep `name`, `description`, and supported standard fields such as `license`
     and `compatibility` in `SKILL.md` frontmatter.
   - Move `version`, `intent`, `tags`, `inputs_schema`, `outputs_schema`,
     `relationships`, `token_estimate`, `maturity_score`, and `security_score`
     into `aptitude.yaml`. `aptitude.yaml` is a sibling of `SKILL.md`; Aptitude
     metadata must not be nested in `SKILL.md` frontmatter.
   - Require a semantic version and `create_skill` or `publish_version`. Check
     the registry before choosing intent; ask when identity remains ambiguous.
   - Move useful `README.md` material into `SKILL.md` or `references/`; do not
     leave `README.md` in the draft.
4. Search with `aptitude_search_skills` for capabilities related to the source.
   Inspect plausible matches with `aptitude_inspect_skill`. Propose exact or
   constrained relationships with reasons; do not add them until the user
   reviews the dependency set.
5. Run local structural validation: kebab-case folder/name match, required
   `SKILL.md`, non-empty trigger-oriented description, valid `aptitude.yaml`
   fields and types, valid semantic version/intent, valid relationship selectors,
   readable relative references, no unsafe links, and no forbidden `README.md`.
   If local structural validation fails, stop before approval and report the exact issues.
6. Preview source and draft paths, coordinate, intent, dependencies, changed or
   relocated files, structural validation, and warnings. Use the
   [shared action-reporting reference](../references/action-reporting.md). Ask for
   explicit approval before replacement.
7. After approval, verify the source has not changed from the recorded checksums.
   If changed, regenerate the draft and preview again. Otherwise move the draft
   to a temporary sibling path, move the source to a temporary sibling backup,
   and move the reviewed draft to the original source path.
8. Validate the final location. On failure, restore the backup and report the
   blocker. On success, keep the backup until the user separately authorizes
   deletion. The converted skill must not contain `draft/`.

## Example

For `skills/code-review/`, create `skills/code-review/draft/`, migrate Aptitude
fields to its `aptitude.yaml`, research relevant dependencies, and show the full
replacement preview. Only approval permits replacing `skills/code-review/`.

## Troubleshooting

- Missing version or uncertain registry identity: ask; do not invent it.
- Unsafe links or unreadable files: stop before drafting.
- Failed final validation: restore the sibling backup automatically.
