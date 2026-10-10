# ADR-0046 | Publish by trusted publishing rather than a stored key

🌍 🇬🇧 English (this file) · 🇫🇷 [Français](0046-publish-by-trusted-publishing-rather-than-a-stored-key.fr.md)

**Status:** Proposed
**Proposed:** 2026-10-10
**Decision Makers:** Reefact

## Context

[ADR-0044](0044-release-each-package-from-its-own-tag.md) has a workflow publish fourteen packages to
nuget.org when a tag is pushed. To do so the workflow has to prove to nuget.org that it acts for the owner of
the packages. That ADR names a stored NuGet API key, held as a repository secret, as the way: its rationale
says a pushed tag fails without it, and its follow-up actions list creating that secret.

A NuGet API key is long-lived, has an expiry the maintainer must remember, and stays valid wherever it leaks.
nuget.org offers another way, **trusted publishing**: the workflow asks GitHub for a signed identity token, nuget.org
checks it against a policy naming a repository and a workflow file, and returns an API key that lives one
hour. NuGet's own documentation presents it as the better way to publish.

The maintainer publishes the packages of another repository, `just-dummies`, this way already: a pinned
`NuGet/login` action, the `id-token: write` permission, and the nuget.org user name held as a repository
*variable*, since it is public. That repository's pipeline is the worked example.

The policy belongs to a repository and a workflow file name, not to a package id, so one policy covers every
package of this repository. An id nobody owns yet is reserved for the account by its first successful push.

## Decision

The release workflow authenticates to nuget.org by trusted publishing, exchanging its GitHub identity for a
short-lived key, and no NuGet key is stored in the repository.

## Rationale

Nothing has to be remembered. A stored key expires, and the day it does the release fails for a reason
unrelated to the release; a key minted for the run does not exist the hour after. Nothing can leak from the
repository's settings either, because there is nothing to leak.

It is how the maintainer's other repository already publishes, so there is one way to do it rather than two,
and its worked example is known to run.

The login is asked for before any work and on a rehearsal as well, so a missing policy or a missing user name
fails in seconds, on the run meant to find it, instead of after the build or during a real release. The key
lives an hour and the run takes minutes, so asking early costs nothing.

The user name is held as a repository variable because it is an identifier, not a credential; stored as a
secret it would only be masked in the logs, which makes a failed login harder to read and protects nothing.

This replaces one detail of ADR-0044 and leaves its decision standing: that a release is a tag, how a tag maps
to packages, and the cascade. Only the mechanism its rationale and follow-up actions name for authenticating —
a stored `NUGET_API_KEY` secret — is replaced.

## Alternatives Considered

### A stored NuGet API key

What ADR-0044 names. Considered because it is the commonest way and takes five minutes to set up.

Rejected because of the expiry, which turns into a failure on the day of a release, and because a key is a
credential that can be read by anything with access to the repository's settings.

### Publish by hand from a maintainer's machine

Considered because it needs no automation.

Rejected because ADR-0044 exists to make a release one pushed tag, and a manual push would make the tag a
statement that nothing guarantees.

## Consequences

### Positive

* No credential is stored, rotated or renewed.
* The rehearsal checks the policy as well as the pipeline.
* One way to publish across the maintainer's repositories.

### Negative

* Setting it up needs the package owner's authenticated session on nuget.org; no one can do it for them.
* A third-party action, `NuGet/login`, sits in the release path. It is pinned to a commit like every other.
* Until the policy and the variable exist, every run of the workflow fails at the login, rehearsal included.

### Risks

* The policy names the repository and the workflow file. Renaming either breaks publishing until the policy
  is changed on nuget.org.
* An id that someone else already holds on nuget.org cannot be published, and is only found at the first push.

## Follow-up Actions

* Create the trusted publishing policy on nuget.org and the `NUGET_USER` variable on GitHub, as set out in
  *Releasing* in `CONTRIBUTING.md`.
* Check that no one else holds a `DesignPatternCatalog.` id on nuget.org before the first tag.

## References

* [ADR-0044](0044-release-each-package-from-its-own-tag.md) — the release mechanism whose authentication
  detail this replaces
* `.github/workflows/release.yml`, and the *Releasing* section of `CONTRIBUTING.md`
* NuGet, *Trusted Publishing* — `learn.microsoft.com/nuget/nuget-org/trusted-publishing`
