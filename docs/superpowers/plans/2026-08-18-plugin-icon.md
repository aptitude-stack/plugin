# Plugin Icon Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Aptitude plugin icon with the supplied transparent SVG without modifying it.

**Architecture:** Keep the existing manifest contract and replace only `assets/favicon.svg` with the provided SVG source. No runtime or plugin behavior changes.

**Tech Stack:** SVG asset, JSON manifest, Python `unittest`.

---

### Task 1: Replace and verify the plugin icon

**Files:**
- Modify: `plugin/plugins/aptitude/assets/favicon.svg`
- Verify: `plugin/plugins/aptitude/.codex-plugin/plugin.json`
- Test: `plugin/tests/test_plugin.py`

- [x] **Step 1: Copy the supplied SVG unchanged**

Run from the workspace root:

```bash
cp "docs/resources/logo Background Removed.svg" "plugin/plugins/aptitude/assets/favicon.svg"
```

- [x] **Step 2: Verify the asset is byte-identical to the supplied source**

Run:

```bash
cmp "docs/resources/logo Background Removed.svg" "plugin/plugins/aptitude/assets/favicon.svg"
```

Expected: exit status `0` and no output.

- [x] **Step 3: Run the existing plugin contract test**

Run from `plugin`:

```bash
UV_CACHE_DIR=.uv-cache uv run python -m unittest tests.test_plugin -v
```

Expected: all tests pass, including the checks that both `logo` and `composerIcon` point to `./assets/favicon.svg`.
