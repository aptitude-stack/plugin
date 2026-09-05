---
name: publish-skill
description: Use when a user requests publishing a local skill to the Aptitude registry, or when a reviewed local inspection is ready for publication.
---

# Publish Aptitude Skill

This is the approval and mutation workflow. If no selected path/registry target
and reviewed inspection exist, use
[inspect-for-publish](../inspect-for-publish/SKILL.md) first. Do not duplicate
discovery or publish a guessed path.

Use the Aptitude Publisher MCP. Do not construct registry HTTP requests or
upload bundles yourself. The Publisher reuses a fresh receipt or, under the
approved plan, auto-refreshes stale or missing evidence. It may then continue
without a second confirmation only when the exact confirmed identity still matches
and the refreshed result is allowed. If identity changes or the result is blocked, do not upload
or report success.
Use the [shared action-reporting reference](../references/action-reporting.md) for the user-facing result.

After the user selects a candidate and registry target, treat the inspection
report as the publication preview:

1. Show the exact reviewed local path, slug, version, intent, registry target,
   scores, gates, and warnings. Ask for one explicit confirmation (one approval)
   of that full publication plan. Require the payload's `skill_path`, `slug`, `version`, `intent`, and
   `registry_url` to match the preview.
2. After approval, call `aptitude_publisher_publish_skill` with the exact
   reviewed identity and target. Keep the registry target unchanged from
   preview through publish:

   ```json
   {
     "skill_path": "<skill-path>",
     "slug": "<evaluated-slug>",
     "version": "<reviewed-version>",
     "intent": "<evaluated-intent>",
     "registry_url": "<reviewed-registry-url>",
     "confirm_upload": true
   }
   ```

Do not print, repeat, or store tokens; the publisher reads its documented
environment variables.
