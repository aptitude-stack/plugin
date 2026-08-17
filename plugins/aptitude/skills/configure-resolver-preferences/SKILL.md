---
name: configure-resolver-preferences
description: Use when changing Aptitude resolver selection preferences or local client policy in user or workspace aptitude.toml.
---

# Configure Aptitude Resolver Preferences

Use the Aptitude MCP. Do not put resolver preferences in `AGENTS.md` or other
repository guidance.

1. Call `aptitude_show_policy` first for the target workspace:

   ```json
   {"cwd": "<target-workspace>", "response_format": "json"}
   ```

   Use `layers` for config paths and contributing layers. Use
   `effective_selection` for values and each selection field's source, and
   `effective_policy` for the aggregate policy source.
2. Ask whether the change is for the **user or workspace** configuration. Explain
   the requested values and get **explicit confirmation** before editing that
   `aptitude.toml`.
3. Preserve unrelated TOML fields. Keep these distinct:
   - `[selection]` is soft: `profile` (`balanced`, `low-cost`, `high-trust`),
     `interaction_mode` (`auto`, `always`, `never`), and `candidate_limit`.
   - `[policy]` is hard: `allowed_trust_tiers`,
     `allowed_lifecycle_statuses`, `max_token_estimate`,
     `max_content_size_bytes`, `max_total_token_estimate`, and
     `max_total_content_size_bytes`. It filters legal candidates; it does not
     rank them.
4. You must never silently broaden an existing policy. State any requested relaxation
   explicitly; restrictive layers can still override it.
5. Call `aptitude_show_policy` again with the same `cwd` and
   `response_format: "json"`. After the second policy call, report effective selection
   with each selection field's source, the effective policy with its aggregate policy
   source, and contributing layers. If the target layer did not win, explain why.

Example workspace preference:

```toml
[selection]
profile = "high-trust"
interaction_mode = "never"
```
