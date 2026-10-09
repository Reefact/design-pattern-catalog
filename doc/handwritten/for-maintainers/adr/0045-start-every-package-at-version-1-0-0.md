# ADR-0045 | Start every package at version 1.0.0

🌍 🇬🇧 English (this file) · 🇫🇷 [Français](0045-start-every-package-at-version-1-0-0.fr.md)

**Status:** Accepted
**Proposed:** 2026-10-09
**Accepted:** 2026-10-09
**Decision Makers:** Reefact

## Context

[ADR-0021](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.md) fixes Semantic Versioning over
two contracts and adds that the packages **stay below `1.0.0`** until no catalogued pattern is expected to
move catalogue: a pattern sits in `Idioms` because no body of work claims it yet, and the day one does it
changes namespace and package both. `CONTRIBUTING.md` draws the consequence: below `1.0.0` its table applies
one step down, a breaking change moving the minor and everything else the patch.

Nothing has been published, and the version is a development placeholder.

[ADR-0044](0044-release-each-package-from-its-own-tag.md) releases each package from its own tag and decides,
for a tag of `Core`, whether every other package takes a patch or the next major. Under the `0.x` convention
that decision would have a different meaning for every version range, and the planner a second table to hold.

`Idioms` holds two patterns. The table in `CONTRIBUTING.md` already lists moving a pattern between catalogues
as a major change.

## Decision

Every package's first release is `1.0.0`, and the packages are versioned from there with the full table.

## Rationale

A version starting at `1.0.0` means the same thing for every package from the first tag: a major step is
breaking, a minor is an addition, a patch reaches no consumer. The convention for `0.x` makes the meaning of
a number depend on which side of `1.0.0` it falls, and the release planner of ADR-0044 would have to know
both.

The cost ADR-0021 was guarding against is real and is accepted: a pattern that moves out of `Idioms` into a
catalogue of its own changes its namespace and its package, and from `1.0.0` that is a major release of
`Idioms` and of the meta-package. It was already a major change in the table; what changes is that it is no
longer excused by a version that promised nothing. Two patterns live in `Idioms`, so the exposure is small
today.

This replaces ADR-0021 on one point only. Semantic Versioning over what a consumer compiles against and what
it reads back stands, and so does everything else ADR-0021 argues; only its clause that the packages stay
below `1.0.0` is superseded.

## Alternatives Considered

### Stay below `1.0.0` until the catalogues stop moving

ADR-0021's position. Considered because it states honestly that the vocabulary is young.

Rejected because the release rules would then carry two meanings for a number, and because the exposure it
guards against is two patterns in `Idioms`.

### Start at `1.0.0` for `Core` and `0.x` for the catalogues

Considered because the catalogues are the part still growing.

Rejected because the cascade moves them together with `Core`, and their numbers would have to cross `1.0.0`
at a moment nothing in the code marks.

## Consequences

### Positive

* One reading of every version number, for every package, from the first release.
* The release planner holds one table.

### Negative

* A pattern leaving `Idioms` is a major release of `Idioms` and of the meta-package.
* `CONTRIBUTING.md` no longer carries the `0.x` paragraph, and until this record is accepted it disagrees with
  ADR-0021.

### Risks

* A consumer reads `1.0.0` as a promise that nothing will move. The table says what a major change is, and a
  pattern leaving a catalogue is one.

## Follow-up Actions

* Decide whether ADR-0021 is marked as superseded, or left as it is with this record naming the one clause it
  replaces.

## References

* [ADR-0021](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.md),
  [ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.md),
  [ADR-0044](0044-release-each-package-from-its-own-tag.md)
