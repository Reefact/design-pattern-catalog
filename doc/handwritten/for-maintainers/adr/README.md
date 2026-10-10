# Architecture Decision Records

Dated records of significant decisions — their context, the option chosen, and
the consequences. An ADR is a historical log: once accepted it is not edited in
place; a decision is revisited by writing a **new** ADR that supersedes the old
one, and the old one's status changes to *Superseded* with a link to its
successor.

## Records 0001 to 0018 were written as one set

Those eighteen carry the same proposal date, and were accepted on that same day.
They were written together, after the decisions they describe had been taken
together, and they describe one coherent position rather than a sequence of
revisions. **None of them amends, refines or supersedes another**, and their
numbering is an index, not a chronology.

Where one of them argues against a shape this repository briefly held, that shape
appears under *Alternatives Considered*, which is where an option weighed and set
aside belongs — not under a superseding record, which is a different instrument.

From ADR-0019 onwards the base grows one decision at a time. Revisiting a record
means writing its successor, never editing it in place: the successor is drafted
as *Proposed*, and only the maintainer moves the record it replaces to
*Superseded*.

That instrument has been used four times, and the four are worth reading together
because they are one line of reasoning rather than four repairs. **ADR-0019 supersedes
ADR-0005** on the identity climb. **ADR-0027** then supersedes ADR-0019 itself, along
with **ADR-0025**, by making each catalogued work an independent package with no
relation across works — which leaves the climb with one mechanism instead of two, and
leaves the reach-back with nothing to reach. **ADR-0028 supersedes ADR-0006**, because
once the catalogues no longer refer to one another, what each of them holds has to be
decided without appeal to the others.

A fifth, **ADR-0045 on ADR-0021**, is of another kind: it replaces a single clause (that the
packages stay below `1.0.0`) and leaves the rest of ADR-0021 standing, which the status line of
ADR-0021 says in so many words.

A superseded record is never edited and never removed. ADR-0019 is both a superseder
and superseded, which is what the chain should look like: each record says what was
believed when it was written.

## When is an ADR written?

Every pull request is checked against this base — the moment new decisions enter
the codebase. Most pull requests embark no architectural decision and add no ADR;
the check is what is mandatory, not the artifact. The test for "significant": *if
the implementation changed but the decision stood, the ADR should not need
editing.* A new decision is **recorded** here, a decision that replaces another is
written as a **superseding** ADR, and a change that **conflicts** with an accepted
ADR is raised for the maintainer. The agent procedure — draft as *Proposed*, never
flip a status unilaterally — is in [`AGENTS.md`](../../../../AGENTS.md), and the
decision that makes the check mandatory is
[ADR-0001](0001-check-every-pull-request-against-the-adr-base.md).

This base carries a particular weight in this repository. The attributes are
generated from a catalog, so almost nothing here is defended by the code itself:
the same generator would happily emit a different shape, and a reader of the
output cannot tell which of its traits were decided and which merely happened.
The reasoning lives here or nowhere.

## An ADR is a decision record, not a specification

An ADR captures a **decision and the reasoning behind it** — not how that
decision is implemented. Implementation mechanics (code, configuration, exact
flags, command snippets, step-by-step walkthroughs) live in the code, in the
catalog, and in the reference documentation the ADR links to — never in the ADR
itself. In particular, **Rationale is argument, not a design document**: if a
paragraph explains *how something is built* rather than *why the decision is
right*, it belongs elsewhere and the ADR links to it.

## File conventions

* One file per decision, under `doc/handwritten/for-maintainers/adr/`, named
  `NNNN-short-title.md` — a four-digit sequence number and a lowercase,
  kebab-case title.
* ADRs are written in **English** — the canonical version — with a French
  translation kept alongside as `NNNN-short-title.fr.md`. The English version is
  authoritative; the French one follows it. Each file carries a language banner
  linking to its counterpart.
* Every ADR follows the format below; [`template.md`](template.md) is a
  copy-ready skeleton.

## Format

### Title and header

```markdown
# ADR-{number} | {Short Title}

**Status:** Proposed | Accepted | Superseded | Deprecated
**Proposed:** YYYY-MM-DD
**Accepted:** YYYY-MM-DD
**Decision Makers:** {Names or team}
```

The header carries **one dated line per state the decision actually reached in
this repository**, and no date is ever overwritten. A record drafted as
*Proposed* carries `Proposed:` alone; accepting it adds `Accepted:` below and
leaves the first line untouched. A supersession moves no date and introduces
none — what connects the two records is the link, not the date.

### Context

Everything that led to the decision, so that someone unfamiliar with the project
understands why a decision had to be made. **Facts only** — it does not justify
the chosen solution. Everything the Rationale argues from must appear here first.

### Decision

**One single sentence.** No justification, no alternatives, no history.

### Rationale

Why this decision is the best choice given the Context. Each argument traces back
to a fact already stated there. **Argument only** — naming a mechanism's role and
why it exists belongs here; documenting how it is wired does not.

### Alternatives Considered

Every serious alternative, each with **why it was considered** and **why it was
ultimately rejected** — not simply that it was.

### Consequences

Under **Positive**, **Negative** and **Risks**.

### Follow-up Actions

Work that becomes necessary because of the decision.

### References

Related ADRs, sources, catalog entries, code.

## Index

| ADR | Title | Status |
|---|---|---|
| [ADR-0001](0001-check-every-pull-request-against-the-adr-base.md) | Check every pull request against the ADR base | Accepted |
| [ADR-0002](0002-keep-the-pattern-catalog-as-data-and-generate-the-attributes.md) | Keep the pattern catalog as data and generate the attributes from it | Accepted |
| [ADR-0003](0003-give-each-role-its-own-attribute-nested-in-its-pattern.md) | Give each role its own attribute, nested in the pattern it belongs to | Accepted |
| [ADR-0004](0004-keep-the-attribute-base-a-pure-marker.md) | Keep the attribute base a pure marker | Accepted |
| [ADR-0005](0005-relate-patterns-by-inheritance-and-read-identity-from-it.md) | Relate patterns by inheritance, and read a pattern's identity from it | Superseded by [ADR-0019](0019-stop-the-identity-climb-at-the-pattern-boundary.md) |
| [ADR-0006](0006-catalogue-a-pattern-where-the-work-that-named-it-put-it.md) | Catalogue a pattern where the work that named it put it | Superseded by [ADR-0028](0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.md) |
| [ADR-0007](0007-decide-sameness-by-the-assertions-a-pattern-carries.md) | Decide that two patterns are the same by the assertions they carry | Accepted |
| [ADR-0008](0008-bind-participants-with-typed-links.md) | Bind participants of one pattern occurrence with typed links | Accepted |
| [ADR-0009](0009-let-each-role-declare-what-it-applies-to.md) | Let each role declare what it can be applied to | Accepted |
| [ADR-0010](0010-annotate-the-declaration-that-introduces-a-role.md) | Annotate the declaration that introduces a role | Accepted |
| [ADR-0011](0011-leave-out-what-cannot-be-annotated.md) | Leave out of the catalog what cannot be annotated | Accepted |
| [ADR-0012](0012-show-every-pattern-at-work-in-a-business-example.md) | Show every pattern at work in a business example | Accepted |
| [ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.md) | Shelve a pattern without a body of work of its own under Idioms | Accepted |
| [ADR-0014](0014-write-commit-messages-to-a-checkable-convention.md) | Write commit messages to a convention a script can check | Accepted |
| [ADR-0015](0015-turn-a-warning-into-an-error-in-ci.md) | Turn a warning into an error in CI | Accepted |
| [ADR-0016](0016-prove-the-sources-are-what-the-catalog-generates.md) | Prove on every pull request that the sources are what the catalog generates | Accepted |
| [ADR-0017](0017-pin-every-action-to-a-commit.md) | Pin every GitHub action to a commit | Accepted |
| [ADR-0018](0018-hold-the-public-surface-to-a-committed-baseline.md) | Hold the public surface to a committed baseline | Accepted |
| [ADR-0019](0019-stop-the-identity-climb-at-the-pattern-boundary.md) | Stop the identity climb at the pattern boundary | Superseded by [ADR-0027](0027-ship-one-independent-package-per-catalogued-work.md) |
| [ADR-0020](0020-cover-a-generated-shape-with-fixtures-not-a-catalog-entry.md) | Cover a generated shape with fixtures, not with a catalog entry | Accepted |
| [ADR-0021](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.md) | Version what a consumer reads, and not only what it compiles | Superseded by [ADR-0045](0045-start-every-package-at-version-1-0-0.md), on one clause only |
| [ADR-0022](0022-admit-a-pattern-of-test-design-to-the-catalog.md) | Admit a pattern of test design to the catalog | Accepted |
| [ADR-0023](0023-admit-an-anti-pattern-on-the-same-terms-as-any-pattern.md) | Admit an anti-pattern on the same terms as any pattern | Accepted |
| [ADR-0024](0024-admit-a-model-of-the-business-to-the-catalog.md) | Admit a model of the business to the catalog | Accepted |
| [ADR-0025](0025-let-an-earlier-work-reclaim-a-pattern-from-a-later-catalog.md) | Let an earlier work reclaim a pattern from a later catalog | Superseded by [ADR-0027](0027-ship-one-independent-package-per-catalogued-work.md) |
| [ADR-0026](0026-follow-an-authors-own-supersession-of-a-catalogued-chapter.md) | Follow an author's own supersession of a catalogued chapter | Accepted |
| [ADR-0027](0027-ship-one-independent-package-per-catalogued-work.md) | Ship one independent package per catalogued work | Accepted |
| [ADR-0028](0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.md) | Hold a pattern in every catalogue whose work presents it as its own | Accepted |
| [ADR-0029](0029-admit-enterprise-integration-patterns-as-a-catalogue.md) | Admit Enterprise Integration Patterns as a catalogue | Accepted |
| [ADR-0030](0030-relate-only-the-narrowings-a-work-states-outright.md) | Relate only the narrowings a work states outright | Accepted |
| [ADR-0031](0031-carry-no-generator-machinery-for-an-unused-capability.md) | Carry no generator machinery for an unused capability | Accepted |
| [ADR-0032](0032-admit-xunit-test-patterns-as-a-catalogue.md) | Admit xUnit Test Patterns as a catalogue | Accepted |
| [ADR-0033](0033-admit-microservices-patterns-as-a-catalogue.md) | Admit Microservices Patterns as a catalogue | Accepted |
| [ADR-0034](0034-let-a-specialisation-name-the-role-it-narrows.md) | Let a specialisation name the role it narrows | Accepted |
| [ADR-0035](0035-index-the-pattern-language-and-require-a-write-up.md) | Index the pattern language, and admit on a write-up rather than a book citation | Accepted |
| [ADR-0036](0036-admit-posa2-as-a-catalogue.md) | Admit Pattern-Oriented Software Architecture Volume 2 as a catalogue | Accepted |
| [ADR-0037](0037-admit-the-dependency-injection-catalogue.md) | Admit the Dependency Injection catalogue, with its lifestyles but not its code smells | Accepted |
| [ADR-0038](0038-name-the-packages-after-the-catalogue-rather-than-the-vendor.md) | Name the packages after the catalogue rather than after the vendor | Accepted |
| [ADR-0039](0039-name-the-attribute-base-after-what-it-marks.md) | Name the attribute base after what it marks | Accepted |
| [ADR-0040](0040-write-the-pattern-guide-by-hand-in-both-languages.md) | Write the pattern guide by hand, in both languages | Accepted |
| [ADR-0041](0041-hold-a-pattern-named-in-an-authors-later-reference-edition.md) | Hold a pattern named in an author's later reference edition | Proposed |
| [ADR-0042](0042-admit-a-catalogue-for-the-maintainers-own-patterns.md) | Admit a catalogue for the maintainer's own patterns | Accepted |
| [ADR-0043](0043-let-a-role-link-to-a-type-that-is-not-a-role.md) | Let a role link to a type that is not a role | Accepted |
| [ADR-0044](0044-release-each-package-from-its-own-tag.md) | Release each package from its own tag, with Core cascading | Accepted |
| [ADR-0045](0045-start-every-package-at-version-1-0-0.md) | Start every package at version 1.0.0 | Accepted |
| [ADR-0046](0046-publish-by-trusted-publishing-rather-than-a-stored-key.md) | Publish by trusted publishing rather than a stored key | Proposed |
