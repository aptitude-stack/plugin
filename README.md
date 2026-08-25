# Aptitude Codex Plugin

Aptitude is a registry for versioned AI-agent skills. Its resolver searches the registry, applies policy, resolves dependencies, and installs verified skill bundles. Its publisher validates a local skill folder before uploading it to the registry.

This Codex plugin packages four Aptitude workflows plus the resolver and
publisher MCPs: inspect a local skill before publishing, publish a local skill,
inspect a registry skill before installing, and install a registry skill. It
does not replace Aptitude's resolver or publisher; it calls their released
interfaces.

Plugins are installable packages that can combine skills and MCP servers. This
plugin contains the `inspect-for-publish`, `publish-skill`,
`inspect-for-install`, and `install-skill` workflows, plus resolver preference
configuration. See [OpenAI's plugin architecture](https://developers.openai.com/plugins/concepts/plugins).

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

When Codex configures the Aptitude MCPs, provide `APTITUDE_READ_TOKEN`; the
publisher also needs `APTITUDE_PUBLISH_TOKEN`, `OPENAI_API_KEY` for its
evaluator, and optionally `APTITUDE_REGISTRY_URL` for a custom registry target.
Do not put credentials in this repository.

## How to use

### Install a skill

Ask Codex to inspect a registry skill before installing it. The
`inspect-for-install` workflow searches, inspects, and resolves
without installing project/skill files or mutating the registry; advisory cache
updates may occur. Then the `install-skill` workflow previews destinations and
asks for confirmation. You must provide the selected coordinate, target agent,
and scope before it writes files.

### Publish a skill

Ask Codex to inspect a local skill folder before publishing it. The
`inspect-for-publish` workflow evaluates it locally and reports validation,
gates, canonical scores, warnings, and receipt metadata without uploading.
Then the `publish-skill` workflow asks for confirmation before
`aptitude_publisher_publish_skill` uploads to the registry.

The publisher reads its publish token from its documented environment variables; never place a token in this repository or a prompt.
