---
name: publish-skill
description: Use when validating and publishing a local skill folder to the Aptitude registry.
---

# Publish Aptitude Skill

Use the Aptitude Publisher MCP. Do not construct registry HTTP requests or upload bundles yourself.

1. Confirm the path is a local skill folder, then call `aptitude_publisher_inspect_skill`:

   ```json
   {"skill_path": "<skill-path>"}
   ```

2. Inspection writes local `.publisher_artifacts/` but does not upload. Stop if it
   returns a blocked result; summarize the evaluated path and result.
3. Review the returned slug, version, intent, validation, gate results, and
   warnings. Get explicit confirmation to publish that same path with its
   explicit slug and `create_skill` or `publish_version` intent.
4. Call `aptitude_publisher_publish_skill` only after that confirmation:

   ```json
   {
     "skill_path": "<skill-path>",
     "slug": "<evaluated-slug>",
     "intent": "<evaluated-intent>",
     "confirm_upload": true
   }
   ```

For validation-only requests, stop after inspection. Do not print, repeat, or store tokens; the publisher reads its documented environment variables.
