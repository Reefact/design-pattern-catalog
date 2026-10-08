# ADR-0041 | Hold a pattern named in an author's later reference edition

🌍 🇬🇧 English (this file) · 🇫🇷 [Français](0041-hold-a-pattern-named-in-an-authors-later-reference-edition.fr.md)

**Status:** Accepted
**Proposed:** 2026-08-12
**Accepted:** 2026-10-08
**Decision Makers:** Reefact

## Context

`DomainDrivenDesign/DomainEvent` has been catalogued since the Domain-Driven Design
catalogue was written, with a reference reading *Eric Evans, Domain-Driven Design, 2003*.

Writing the pattern guide surfaced a problem with that reference. Domain Event is not a
pattern of the 2003 book: it does not appear in the pattern language the book sets out, and
Evans discusses events there only in passing. The claim rests on the book's own list of what
it names rather than on a reading of the whole text, and is stated here so it can be checked
rather than taken on trust.

Evans names the pattern in *Domain-Driven Design Reference: Definitions and Pattern
Summaries*, 2015. That work is not a new book. It is Evans restating the pattern summaries of
the 2003 book, with a small number of additions made in the eleven years between them —
Domain Events among them. It carries the same vocabulary, the same author and the same
pattern language.

Martin Fowler published a *Domain Event* on his own site in 2005, in the eaaDev material.
That material was examined for admission as a catalogue of its own and the check came out
negative, so nothing in this repository holds it.

[ADR-0028](0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.md) decides that a
pattern is held in every catalogue whose work presents it as one of its own — the test being
authorship, not mention. [ADR-0027](0027-ship-one-independent-package-per-catalogued-work.md)
ships one independent package per catalogued work.
[ADR-0026](0026-follow-an-authors-own-supersession-of-a-catalogued-chapter.md) decides that
where an author states that a later work of his own supersedes part of a catalogued work, the
catalog follows the later work and catalogues it as a catalog of its own. Its precondition —
a stated supersession — is not met here: the Reference does not supersede the book, it
summarises it.

`catalog/pattern.schema.json` describes the reference as load-bearing rather than editorial:
it is what says which work holds the pattern.

Every other catalogue in the repository carries exactly one reference work across all its
entries. The single exception is `Idioms`, which holds two, and which
[ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.md) built precisely as
the catalogue with no corpus of its own.

Nothing is released yet ([ADR-0021](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.md)).

## Decision

A pattern named in an author's later reference edition of a catalogued work is held in that
work's catalogue, and its own reference names the edition that names it.

## Rationale

The reference is what makes the catalog checkable, so an entry whose reference is false is
worse than an entry that is missing. A reader who installs `DesignPatternCatalog.DomainDrivenDesign`,
meets `[DomainEvent]` credited to a 2003 book, and goes looking for it in that book finds
nothing — and has no way to tell whether the catalog is wrong or their reading is. Correcting
the reference is not optional once the discrepancy is known.

The question the correction opens is where the entry then belongs, and the answer follows from
what ADR-0028 made the test. That ADR asks whether a **work presents the pattern as one of its
own** — names it, describes it, gives it a place in its own pattern language. The Reference
does all three. The 2003 book does none of them. So the entry is legitimate, and it is
legitimate on account of the Reference.

Cataloguing the Reference separately, as ADR-0026 does for *Accounting Patterns*, would be the
wrong reading of that ADR. What justified a catalogue of its own there was a **supersession**
stated by the author, and a vocabulary that had genuinely changed: of the fifteen pattern
names in Fowler's chapter 6, one survived into the paper. Nothing of that kind is true here.
The Reference restates the book's vocabulary rather than replacing it, and a `DomainDrivenDesignReference`
package would ship twenty-two entries identical to those of its neighbour in order to house a
twenty-third.

Holding the entry in the Domain-Driven Design catalogue also matches what the packages promise
a reader. ADR-0027's independence claim is that a catalogue is the complete rendering of a
work; for a reader, the work is Evans' Domain-Driven Design, and the Reference is where that
work's vocabulary is now most conveniently found. Splitting one pattern away from the
twenty-two it belongs among would satisfy a rule about editions at the cost of the promise the
rule exists to keep.

Fowler's 2005 page is not a competing claim to resolve. ADR-0028 requires a work that presents
the pattern as its own **and** is catalogued here; the eaaDev material is not catalogued, so
the question of which of the two named it first has no consequence for what this repository
holds. It is recorded above because a reader who knows the history would otherwise wonder
whether it was overlooked.

The precedent this sets is narrow by construction. It applies to a later edition **by the same
author, of the same work**, restating the same pattern language — not to any later work that
mentions a pattern, which is exactly what ADR-0028 already refuses.

## Alternatives Considered

### Leave the reference as *Domain-Driven Design, 2003*

Considered because it costs nothing and keeps every catalogue single-work.

Rejected because it is false, and because the falsehood is the kind the catalog exists to
prevent. The schema calls the reference load-bearing; an entry that misattributes its own
source undermines every other entry's credibility, since a reader has no way to know which
references were checked.

### Catalogue *Domain-Driven Design Reference* as a catalogue of its own

Considered because ADR-0026 did exactly that for *Accounting Patterns*, and following an
existing precedent is cheaper than writing a new record.

Rejected because the precondition differs. ADR-0026 turns on an author's stated supersession
and on a vocabulary that had genuinely diverged; the Reference supersedes nothing and diverges
in one entry. The result would be a package of twenty-three patterns, twenty-two of which
duplicate the neighbouring package, shipped so that one entry can be filed under the edition
that names it.

### Drop the entry from the catalogue

Considered because it restores the invariant that every entry traces to the catalogue's single
work, and because ADR-0011 already leaves out what cannot be annotated.

Rejected because the pattern is annotatable, is used, and is part of the vocabulary a reader
of Domain-Driven Design expects — `MicroservicesPatterns/DomainEvent` exists next door and
credits DDD in its first line. Removing it would make the catalogue less complete in order to
make a rule tidier, and ADR-0028 exists to prevent exactly that trade.

## Consequences

### Positive

* The reference tells the truth, and a reader who follows it finds the pattern.
* ADR-0028's test — does the work present the pattern as its own — is applied rather than
  assumed, and the answer is now recorded.
* The Domain-Driven Design catalogue can be declared complete: twenty-three entries, each with
  a source that holds.
* The pattern guide can carry a Domain Event page, which it declined to write while the source
  was in doubt.

### Negative

* `DomainDrivenDesign` becomes the second catalogue whose entries do not all share one
  reference work, after `Idioms`.
* The generated index shows one row whose work differs from the catalogue heading above it,
  which a reader may take for an error before finding this record.
* A rule that a catalogue has exactly one reference work — plausible to write, and never
  written — is now unavailable.

### Risks

* The claim that Domain Event is absent from the 2003 book rests on the book's own pattern
  list rather than on a full reading. If it is wrong, this record is unnecessary and the
  reference should return to 2003.
* The narrowness of the precedent depends on reading it as written. A later maintainer could
  stretch *later reference edition* to cover any subsequent work by the same author, which
  ADR-0028 already refuses and this record does not intend to reopen.

## Follow-up Actions

* Re-read the 2003 book's pattern list to confirm the absence, if a copy is at hand.
* Decide whether Fowler's eaaDev *Domain Event* deserves a record of its own, given that the
  eaaDev admission check came out negative for reasons unrelated to this pattern.

## References

* [ADR-0006](0006-catalogue-a-pattern-where-the-work-that-named-it-put-it.md) — catalogue a pattern where the work that named it put it
* [ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.md) — shelve a pattern without a body of work under Idioms
* [ADR-0026](0026-follow-an-authors-own-supersession-of-a-catalogued-chapter.md) — follow an author's own supersession of a catalogued chapter
* [ADR-0027](0027-ship-one-independent-package-per-catalogued-work.md) — ship one independent package per catalogued work
* [ADR-0028](0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.md) — hold a pattern in every catalogue whose work presents it
* [ADR-0040](0040-write-the-pattern-guide-by-hand-in-both-languages.md) — write the pattern guide by hand, in both languages
* `catalog/pattern.schema.json` — the reference field, and why it is load-bearing
