# Plugin Icon Design

## Scope

Update the Aptitude Codex plugin icon only. Use the supplied background-removed SVG unchanged and keep the existing manifest wiring to `./assets/favicon.svg`.

## Design

- Replace `plugin/plugins/aptitude/assets/favicon.svg` with `docs/resources/logo Background Removed.svg` byte-for-byte.
- Do not edit the supplied SVG or add color transformations.
- Leave the existing manifest metadata and icon paths unchanged.
- Do not add a new icon dependency, duplicate plugin asset, or change plugin behavior.

## Verification

Run the existing plugin unit test and confirm the manifest still points both icon fields to the SVG asset.
