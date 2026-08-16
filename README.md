# Aptitude Codex Plugin

Aptitude is a registry for versioned AI-agent skills. Its resolver searches the registry, applies policy, resolves dependencies, and installs verified skill bundles. Its publisher validates a local skill folder before uploading it to the registry.

This Codex plugin packages both workflow instructions and the Aptitude resolver MCP: find and install a skill through Aptitude, or inspect and publish a local skill. It does not replace Aptitude's resolver or publisher; it calls their released interfaces.

Plugins are installable packages that can combine skills and MCP servers. This plugin contains the `install-skill` and `publish-skill` skills plus the resolver MCP. See [OpenAI's plugin architecture](https://developers.openai.com/plugins/concepts/plugins).

## How to install

Add this repository as a Git-backed marketplace:

```sh
codex plugin marketplace add aptitude-stack/plugin --sparse .agents/plugins --sparse plugins/aptitude
```

Restart the ChatGPT desktop app, open the Plugins Directory, choose the **Aptitude** marketplace, and install the **Aptitude** plugin. The marketplace resolves the plugin from `plugins/aptitude`.

To refresh it after a new release:

```sh
codex plugin marketplace upgrade aptitude
```

For local development instead, run this command from a checkout of this repository:

```sh
codex plugin marketplace add ./
```

Restart the desktop app and install from the local **Aptitude** marketplace. OpenAI documents Git and local marketplace sources, including sparse checkouts, in its [plugin packaging guide](https://developers.openai.com/plugins/build/plugins).

When Codex configures the Aptitude MCP, provide `APTITUDE_READ_TOKEN`. Do not put it in this repository.

## How to use

### Install a skill

Ask Codex to find and install an Aptitude skill. The `install-skill` workflow searches, inspects, resolves, and previews destinations before it asks for confirmation. You must provide the target agent and scope before it writes files.

### Publish a skill

Ask Codex to publish a local skill folder. The `publish-skill` workflow runs `aptitude-publisher inspect` first and stops on failed checks. It asks for confirmation before any registry upload.

The publisher reads its publish token from its documented environment variables; never place a token in this repository or a prompt.
