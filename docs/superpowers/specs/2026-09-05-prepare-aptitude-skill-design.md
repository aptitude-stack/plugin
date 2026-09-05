# Prepare Aptitude Skill

## Goal

Add a standalone Aptitude plugin workflow that converts an existing agent skill
into an Aptitude-compatible skill without changing the source until the user
reviews and approves the converted draft.

## Workflow

1. Resolve the exact user-selected skill directory and inspect `SKILL.md` plus
   its non-secret supporting files.
2. Create a complete converted copy at `<skill-root>/draft/`. Exclude an
   existing `draft/`, Publisher artifacts, caches, and secret files.
3. Preserve useful scripts, references, assets, and `agents/openai.yaml`.
4. Keep standard skill fields in `SKILL.md` frontmatter. Move Aptitude fields
   into a sibling `aptitude.yaml` containing the version, intent, tags, schemas,
   relationships, token estimate, maturity score, and security score when those
   values are known.
5. Do not invent missing identity or relationship data. Check the registry to
   distinguish `create_skill` from `publish_version`, and ask the user when the
   version or intent remains ambiguous.
6. Search and inspect registry skills that plausibly complement the source
   skill. Propose only evidence-backed relationships and let the user review the
   dependency set before writing it into the draft.
7. Move useful `README.md` material into `SKILL.md` or `references/`; Publisher
   rejects a `README.md` inside a publishable skill directory.
8. Validate the draft locally against the documented skill-folder and
   `aptitude.yaml` contracts. Do not call Aptitude Publisher or run external
   evaluators in this workflow.
9. Preview the source and draft paths, exact coordinate and intent, proposed
   relationships, file changes, structural validation result, and warnings.
10. Ask for explicit approval to replace the source with the reviewed draft.

## Replacement Safety

Before replacement, verify that the source still matches the state used to
create the preview. If it changed, regenerate the draft and require a new
preview.

After approval, move the original skill to a temporary sibling backup, move the
draft into the original path, and validate the final location. Restore the
backup automatically if replacement or validation fails. Keep a successful
backup until the user explicitly requests its deletion.

The replacement must remove files absent from the reviewed draft and must not
leave a nested `draft/` directory in the converted skill.

## Plugin Integration

Create one self-contained workflow skill under
`plugins/aptitude/skills/prepare-aptitude-skill/SKILL.md`. Reuse the existing
Resolver discovery interfaces for dependency research instead of adding a new
MCP server, conversion script, or registry API client.

Update the plugin description, prompts, README, patch version, and existing
contract test only where needed to expose and verify the new workflow. No
registry publication, plugin release, commit, or marketplace update is part of
this change.

## Error Handling

- Stop when the source path is missing, ambiguous, or contains unsafe links or
  unreadable files.
- Do not read dotenv files, credentials, Publisher artifacts, or caches.
- Stop when a required version or intent remains unresolved.
- Treat dependency discovery as advisory; do not add a relationship without
  user review.
- Stop when local structural validation fails and report the exact issue.
- Roll back the replacement if final-location validation fails.

## Verification

The skill is developed with the documentation TDD workflow:

1. Extend the plugin contract test first and verify it fails because the new
   skill and plugin metadata are absent.
2. Add the minimum workflow instructions and metadata changes needed to pass.
3. Run the focused plugin test, full plugin test suite, smoke test, skill
   validator, and `git diff --check`.
4. Forward-test the completed skill with the same pressure scenario used for
   the baseline and verify that it uses `aptitude.yaml`, rejects nested
   Aptitude metadata in `SKILL.md`, handles `README.md`, targets the correct
   plugin path, preserves the source until approval, and never publishes.

## Explicit Non-Goals

- Publishing the converted skill to the registry.
- Running Aptitude Publisher inspection or external evaluators.
- Automatically accepting dependency suggestions.
- Modifying the original skill before approval.
- Adding a conversion framework, persistent state, or new MCP tool.
- Deleting the successful rollback backup without separate authorization.
