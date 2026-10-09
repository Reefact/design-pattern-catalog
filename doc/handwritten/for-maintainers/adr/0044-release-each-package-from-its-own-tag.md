# ADR-0044 | Release each package from its own tag, with Core cascading

🌍 🇬🇧 English (this file) · 🇫🇷 [Français](0044-release-each-package-from-its-own-tag.fr.md)

**Status:** Accepted
**Proposed:** 2026-10-09
**Accepted:** 2026-10-09
**Decision Makers:** Reefact

## Context

**Nothing is published.** The version is a development placeholder, one number for every package, held in
`build/Packaging.props`, and no workflow publishes anything: the CI packs the solution to prove it can be
packed and stops there.

There are fourteen packages. `Core` holds the base marker and is referenced by every catalogue. Twelve
catalogues each carry one work, independent of the others
([ADR-0027](0027-ship-one-independent-package-per-catalogued-work.md)). A meta-package holds no code and
references all thirteen, so that a consumer who wants everything installs one package.

ADR-0027 chose independent packages for their churn: a change to one work should not republish the others.
It also prescribed that **the first release version them in lockstep**, because loosening later is easy and
tightening later is not.

**A change to `Core` reaches every package.** Its reading rules decide what every annotation in every
catalogue means to a consumer's reader, and every catalogue depends on it. A change to the generator template
or to `Packaging.props` reaches every package too.

The meta-package depends on its thirteen packages at exact versions, so it must be republished whenever one
of them is.

Whether a change is breaking is a judgement about what a consumer compiles against and what it reads back
([ADR-0021](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.md)). No tool derives it.

## Decision

A package is released from a tag that carries its own name and version: a tag of `Core` releases every
package, a tag of a catalogue releases that catalogue and the meta-package, and a tag of the meta-package
releases it alone.

## Rationale

The tag is the one place a release is stated, so it is the one input. A version kept in a committed file as
well would be a second statement of what shipped, free to disagree with the first; here the numbers of the
packages a tag does not name are read from their own last tags, and nothing else.

Independent tags give the churn benefit ADR-0027 was chosen for: a new pattern in one catalogue republishes
that catalogue and the meta-package, not twelve packages whose content did not change.

A tag of `Core` cascades because a change to it is a change to everyone. What each package moves to follows
the step the maintainer gave `Core`: a major step is breaking, and every package takes the next major; any
other step is not, and every package takes the next patch. The workflow cannot judge breakage, but the
maintainer already does when choosing the number, and the cascade reads that choice rather than asking for it
twice. A number that is not exactly one step above the previous tag of its package is refused, so a typo
cannot pass for a decision.

The meta-package follows the level of the step that triggered it, so a patch to a catalogue is a patch to the
meta-package and a new minor is a minor. A catalogue's very first tag, which adds a dependency, is a minor.

The first release is a tag of `Core` at `1.0.0`. Every package has no previous version, so the cascade
releases all of them at `1.0.0`, which is the lockstep ADR-0027 asked for, reached without a mechanism of its
own. Later releases loosen it, as that ADR foresaw.

The version is read per project, by project name, from a file the planner writes for the release. That is
what makes a project reference become a dependency on the version that project is released at; a single
global version would give every dependency the number of the package being packed.

A tag must point at a commit of `main`, and the workflow runs the tests before it packs. Without a NuGet key
it is a dry run, so it can be exercised before a key exists.

## Alternatives Considered

### One tag releases everything at one version

The lockstep of ADR-0027, kept. Considered because it is the simplest thing to get right and the planner
would be trivial.

Rejected as a permanent rule: a new pattern in one catalogue would republish all fourteen packages, which is
the churn that splitting the catalogues was meant to end. It stays, in effect, for the first release.

### Versions in a committed file

Considered because a version can then be reviewed in a pull request.

Rejected because it makes the file and the tag two statements of one fact, and a release workflow would have
to check they agree. The tag is needed anyway.

### A tag-driven versioning tool

Considered because it exists and is widely used.

Rejected because the cascade needs the next version of packages the tag does not name, which a tool that
reads each project's own tags cannot compute.

## Consequences

### Positive

* A release is one pushed tag.
* A catalogue can ship without the others, and the first release still ships them together.
* The versions on nuget.org are the versions in the tags; nothing else records them.

### Negative

* A change to `Core` republishes all fourteen packages, including ones whose content did not change.
* The workflow creates tags, so it needs permission to write to the repository.
* Fourteen tag prefixes to know.

### Risks

* The breaking-or-not decision is the maintainer's, and a wrong number ships. The planner refuses an invalid
  step, not a wrong one.
* A push that fails partway leaves some packages published and no tags created. The workflow skips a package
  already on nuget.org, so running it again completes the release.
* A catalogue added after the first release has no tag. The meta-package depends on it, so no tag but
  `core-v…` or its own can release anything until it has one; the planner says so.

## Follow-up Actions

* Create the `NUGET_API_KEY` secret, and check that the `DesignPatternCatalog.` identifiers are free on
  nuget.org, before the first tag.
* Update the description and tags of the meta-package, which predate most of the catalogues.

## References

* [ADR-0021](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.md),
  [ADR-0027](0027-ship-one-independent-package-per-catalogued-work.md),
  [ADR-0038](0038-name-the-packages-after-the-catalogue-rather-than-the-vendor.md)
* [ADR-0045](0045-start-every-package-at-version-1-0-0.md) — the version the first release starts at
* `.github/workflows/release.yml`, `tools/release/plan.py`, and the *Releasing* section of `CONTRIBUTING.md`
