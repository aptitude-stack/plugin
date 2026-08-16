# Aptitude Codex Plugin

Aptitude is a registry for versioned AI-agent skills. Its resolver searches the registry, applies policy, resolves dependencies, and installs verified skill bundles. Its publisher validates a local skill folder before uploading it to the registry.

This Codex plugin puts those two workflows in one place: find and install a skill through the Aptitude MCP, or inspect and publish a skill through the Aptitude publisher. It does not replace Aptitude's resolver or publisher; it calls their released interfaces.

## How to install

From this repository root, open the local marketplace in Codex:

```sh
open "$(python3 -c 'from pathlib import Path; from urllib.parse import quote; print("codex://plugins/aptitude?marketplacePath=" + quote(str(Path(".agents/plugins/marketplace.json").resolve()), safe=""))')"
```

Select **Install** for Aptitude. The marketplace maps the local plugin entry to `plugins/aptitude`.

When Codex configures the Aptitude MCP, provide `APTITUDE_READ_TOKEN`.

## How to use

### Install a skill

Ask Codex to find and install an Aptitude skill. The `install-skill` workflow searches, inspects, resolves, and previews destinations before it asks for confirmation. You must provide the target agent and scope before it writes files.

### Publish a skill

Ask Codex to publish a local skill folder. The `publish-skill` workflow runs `aptitude-publisher inspect` first and stops on failed checks. It asks for confirmation before any registry upload.

The publisher reads its publish token from its documented environment variables; never place a token in this repository or a prompt.
