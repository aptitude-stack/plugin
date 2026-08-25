---
name: publish-skill
description: Use when a user requests publishing a local skill to the Aptitude registry, or when a reviewed local inspection is ready for publication.
---

# Publish Aptitude Skill

This is the mutation workflow. If no reviewed inspection exists for the same
path and coordinate, use [inspect-for-publish](../inspect-for-publish/SKILL.md)
first. Do not duplicate that inspection workflow here.

Use the Aptitude Publisher MCP. Do not construct registry HTTP requests or
upload bundles yourself. The Publisher reuses a fresh receipt or, under the
approved plan, auto-refreshes stale or missing evidence. It may then continue
without a second confirmation only when the exact confirmed identity still matches
and the refreshed result is allowed. If identity changes or the result is blocked, do not upload
or report success.
Use the [shared action-reporting reference](../references/action-reporting.md) for the user-facing result.

1. Confirm the reviewed local path, exact slug, version, intent, and exact
   `registry_url`. Require the payload's `skill_path`, `slug`, `version`,
   `intent`, and `registry_url` identity to match the reviewed identity. Get
   explicit confirmation to publish that same coordinate and target; keep the
   registry target unchanged from review through publish.
2. Call `aptitude_publisher_publish_skill` only after that confirmation:

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
