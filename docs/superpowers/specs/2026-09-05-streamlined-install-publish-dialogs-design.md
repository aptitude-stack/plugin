# Streamlined Install and Publish Dialogs

## Goal

Reduce installation and publication to two user decisions while preserving an
exact preview and explicit approval before any mutation.

## Install flow

1. Search and show useful candidates with purpose, scores, warnings,
   dependencies, and fit. Ask once for the selected candidate, target agents,
   and project/global/custom scope (including a custom path when applicable).
2. Inspect and resolve the selected coordinate without installing. Preview the
   exact destinations and full dependency plan, then ask once for approval.
3. Install exactly the reviewed coordinate and destination inputs. Report the
   changed destinations, installed dependencies, warnings, or failure.

No target input may change between preview and installation. If the combined
selection omits required destination information, ask one combined follow-up
rather than separate agent, scope, and path questions.

## Publish flow

1. Discover plausible local skill directories and show what each contains or
   is intended to offer. Ask once for the selected path and registry target.
2. Inspect the selected path without uploading. Preview the exact path, slug,
   version, intent, registry target, scores, gates, and warnings, then ask once
   for approval.
3. Publish exactly the reviewed identity and target. Report the registry result
   or the precise blocker.

A stale receipt may be refreshed only under the existing identity-preserving
rule. An identity or target change requires a new preview and approval.

## Reporting and verification

Candidate choices must be decision-useful, not name-only lists. Preview reports
must distinguish inspection/resolution from mutation. Contract tests will lock
the combined questions, three-phase symmetry, immutable preview inputs, and the
single post-preview approval gate for both workflows.
