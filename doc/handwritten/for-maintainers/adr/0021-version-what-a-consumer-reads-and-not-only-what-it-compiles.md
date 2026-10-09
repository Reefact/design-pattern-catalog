# ADR-0021 | Version what a consumer reads, and not only what it compiles

🌍 🇬🇧 English (this file) · 🇫🇷 [Français](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.fr.md)

**Status:** Superseded by [ADR-0045](0045-start-every-package-at-version-1-0-0.md), on one clause only: that the packages stay below `1.0.0`. The rest of this record stands.
**Proposed:** 2026-08-05
**Accepted:** 2026-08-06
**Decision Makers:** Reefact

## Context

The library now has a package identity and no version policy. `0.1.0-dev` is a
placeholder, and nothing says what a number would mean.

Several records already state, separately, what is additive and what is not.
Adding a role to a published pattern is additive
([ADR-0003](0003-give-each-role-its-own-attribute-nested-in-its-pattern.md)) and
is now guarded by the API baseline
([ADR-0018](0018-hold-the-public-surface-to-a-committed-baseline.md)). Widening a
role's target set is additive while narrowing one breaks consumers who had
annotated legitimately
([ADR-0009](0009-let-each-role-declare-what-it-applies-to.md)). A pattern that
later acquires a body of work moves namespace, which breaks consumers wherever it
started ([ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.md)).
None of these was written as a versioning rule, and together they do not make one.

This library has a second contract that no compiler defends. The attributes carry
no behaviour and the library publishes no reader: a consumer copies the reading
rules and owns them ([ADR-0004](0004-keep-the-attribute-base-a-pure-marker.md)).
Two kinds of change therefore alter what a consumer gets while leaving the public
surface byte-identical:

* **A relation.** Declaring that one pattern declines another changes what
  `IdentityOf` answers for annotations that were already written. A count that
  reported two patterns reports one, and no type was added, removed or renamed
  ([ADR-0005](0005-relate-patterns-by-inheritance-and-read-identity-from-it.md),
  [ADR-0019](0019-stop-the-identity-climb-at-the-pattern-boundary.md)).
* **A reading rule.** ADR-0019 changed how identity is computed. Nothing in the
  assembly changed; every consumer that copies the reader gets different answers
  the next time it copies.

`Inherited` sits in the same place: flipping it changes what a reader finds on a
subtype, and compiles either way.

The catalog is expected to grow by an order of magnitude, and much of that growth
is additive by construction. The moves are not: PoEAA holds two entries of some
fifty, `Idioms` does not exist yet, and both are places from which patterns will
be relocated as the works around them are catalogued.

Nothing has been published, so no consumer is owed anything yet.

## Decision

The package follows Semantic Versioning over both what a consumer compiles against
and what it reads back — so a change to a pattern's identity or to a reading rule
is a major release even when the public surface is untouched — and it stays below
`1.0.0` until no catalogued pattern is expected to move catalog.

## Rationale

Versioning only the surface would be precise and wrong. The whole point of this
library is that a consumer reads meaning out of the types, so a release that keeps
every type and changes what they mean is a breaking release by the only definition
that matters here. The API baseline already makes surface changes visible; what it
cannot see is exactly what this extends the policy to cover.

Stating the mapping is what makes the rule usable rather than aspirational, and
almost all of it is already decided elsewhere — this collects it:

| | |
|---|---|
| **Major** | a role or pattern removed or renamed · a target set narrowed · `AllowMultiple` or `Inherited` changed · a pattern moved between catalogs · a relation added, removed or changed in nature · a reading rule changed |
| **Minor** | a pattern added · a role added to a published pattern · a target set widened · a link added to a role |
| **Patch** | documentation, samples, the catalog index, anything that reaches no consumer |

Two entries in that table are the ones a maintainer will be tempted to get wrong.
A relation looks like an editorial statement about two books and is in fact a
change to every consumer's grouping. A reading rule looks like documentation and
is the thing consumers copy.

Staying below `1.0.0` is honest about which half is unstable. The mechanism is
settled — twenty records argue it, the shape has survived a redesign, and the
convention tests hold it. What is not settled is *placement*: a pattern sits in
`Idioms` because no body of work claims it yet, and the day one does it moves,
which ADR-0013 accepted as a cost. With two catalogs barely started, those moves
are likely and clustered, and spending a major version on each would say the
library is unstable when only its filing is. `0.x` says that plainly and costs
nothing while nothing is published.

The criterion for `1.0.0` is therefore about the catalogs rather than about time
or completeness: it comes when the works a catalogued pattern could belong to are
present, so that a relocation becomes an accident rather than an expectation. That
is a judgement, but it is a judgement about a stated thing, which is what makes it
reviewable.

Below `1.0.0` the rules above still apply, one step down — a breaking change moves
the minor, everything else the patch. Semantic Versioning permits anything in
`0.x`, and permission to break silently is not a policy. Behaving as though the
number mattered is what makes the promotion to `1.0.0` a formality rather than an
event.

## Alternatives Considered

### Version the public surface only, as any library does

Considered because it is what every tool understands, what the API baseline
already tracks, and what a consumer's package manager can act on.

Rejected because it would call a release that changes every consumer's grouping a
patch. The surface is not the product here — the meaning read out of it is — and a
policy that cannot express the difference guarantees that the difference will be
missed.

### Go to `1.0.0` at the first release

Considered because the mechanism is stable, `0.x` reads as "not ready" to a
prospective consumer, and it invites a lower standard of care.

Rejected because it would apply a stable number to a catalog whose filing is
knowingly provisional. The first `Idioms` entry that acquires a body of work is a
major release under this policy, and several of those are expected close together;
a `1.x` that reaches `4.0.0` in a season communicates less than a `0.x` that has
not promised yet.

### Version each catalog separately

Considered because the catalogs move at different speeds, and a consumer using
only the Gang of Four should not be disturbed by Domain-Driven Design churning.

Rejected as a packaging decision disguised as a versioning one: it would require
one package per catalog, which is a much larger change with its own consequences
for the relations that cross catalogs — a declension binds two catalogs by
inheritance. It stays available if the churn ever justifies the split.

### Date-based or sequential releases

Considered because much of the growth is additive, and a catalog release train
reads naturally as a date.

Rejected because it discards the one thing a consumer needs from a version here.
The whole difficulty is that some changes break and look exactly like the ones
that do not; a scheme that refuses to say which is which moves the problem to a
changelog nobody reads before upgrading.

## Consequences

### Positive

* A change that alters what consumers read cannot be released as a patch.
* The scattered claims about what is additive become one table, in one place.
* `0.x` states which half of the library is provisional, instead of implying the
  whole of it is.
* The condition for `1.0.0` is written down, so reaching it is a decision someone
  can argue with rather than a mood.

### Negative

* A relation between two patterns — an editorial judgement — now carries the cost
  of a major release, which will make declaring one feel disproportionate.
* Judging whether a pattern is "expected to move" is not mechanical, so the
  promotion to `1.0.0` will need arguing.

### Risks

* Nothing enforces the meaning half. The API baseline catches a surface change; a
  relation added to the catalog produces a small, innocuous-looking diff, and only
  review connects it to a major version.
* A long `0.x` invites consumers to pin exactly and never upgrade, which is the
  opposite of what a growing vocabulary wants.

## Follow-up Actions

* Take the version from a release tag rather than from the project file, and
  promote the accumulated entries to `PublicAPI.Shipped.txt` at the first release
  (ADR-0018).
* Record the reading rules' own version alongside them, if a consumer ever needs
  to say which revision of the rules its reader implements.

## References

* [ADR-0018](0018-hold-the-public-surface-to-a-committed-baseline.md) — the
  baseline, which sees the half of this that is a surface.
* [ADR-0004](0004-keep-the-attribute-base-a-pure-marker.md) — why a consumer owns
  the reading rules, and why changing them reaches it.
* [ADR-0019](0019-stop-the-identity-climb-at-the-pattern-boundary.md) — a reading
  rule changing, which this classifies.
* [ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.md) — the
  relocation that keeps the version below `1.0.0`.
* `CONTRIBUTING.md` — the table as an author meets it.
