---
name: publish-skill
description: Use when validating and publishing a local skill folder to the Aptitude registry.
---

# Publish Aptitude Skill

Use the released publisher CLI. Do not construct registry HTTP requests or upload bundles yourself.

1. Confirm the path is a local skill folder, then run:

   ```sh
   uvx aptitude-publisher inspect <skill-path>
   ```

2. Stop if inspection fails. Summarize the evaluated path and result.
3. Get explicit confirmation before publishing that same path. Then run:

   ```sh
   uvx aptitude-publisher publish <skill-path>
   ```

Use `--dry-run` when the user asks for validation without an upload. Do not print, repeat, or store tokens; the publisher reads its documented environment variables.
