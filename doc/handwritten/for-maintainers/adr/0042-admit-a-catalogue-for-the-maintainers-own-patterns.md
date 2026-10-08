# ADR-0042 | Admit a catalogue for the maintainer's own patterns

🌍 🇬🇧 English (this file) · 🇫🇷 [Français](0042-admit-a-catalogue-for-the-maintainers-own-patterns.fr.md)

**Status:** Proposed
**Proposed:** 2026-10-08
**Decision Makers:** Reefact

## Context

Ten works are catalogued, plus `Idioms`: **343 patterns, 619 roles**. Every one of the ten is a work
by somebody else, published and read whole or in part; `Idioms` holds patterns that have a source and
no body of work of their own ([ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.md)),
and was kept free of "single-entry catalogs" on purpose.

On 6 October 2026 the maintainer published an article, *Advanced Value Objects in .NET*, on
`reefact.net`. It states a way of building value objects in .NET and names, among its attributes,
four that the catalogue cannot express today: the rehydration method, the dehydration method and the
dehydrated object that crosses the boundary of a value object, and a member opened to one named
collaborator. The catalogue holds `ValueObject` twice — Evans', and Fowler's in *Patterns of Enterprise
Application Architecture* — and neither says anything about how a value object crosses a boundary or
who may call what it hides.

Four constraints bear on where such patterns can go.

* A pattern is held by every catalogue whose work presents it as its own
  ([ADR-0028](0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.md)). Evans' book does not
  present these four, so `DomainDrivenDesign` cannot hold them.
* A relation never crosses a catalogue, each catalogued work being an independent package
  ([ADR-0027](0027-ship-one-independent-package-per-catalogued-work.md)). A pattern admitted to a new
  catalogue cannot narrow `ValueObject`.
* Packages are named after the catalogue rather than the vendor
  ([ADR-0038](0038-name-the-packages-after-the-catalogue-rather-than-the-vendor.md)).
* `Idioms` is the place ADR-0013 provides for a pattern with a source and no catalogue of its own. The
  article is not an index gloss: it carries, for each of the four, a problem, a solution and named
  participants, the bar [ADR-0035](0035-index-the-pattern-language-and-require-a-write-up.md) applies.

The article is not the last text the maintainer will write, and the attributes it names are not the only
ones used day to day that no catalogued work names. The maintainer has said the catalogue should hold all
of them.

## Decision

A catalogue named `Reefact` holds the patterns its maintainer uses that no catalogued work names, each
entered with the text that presents it — an article, a chapter, a talk — as its reference.

## Rationale

The gap is real and cannot be filled elsewhere. ADR-0028 settles the question of whose it is: the work
that presents the pattern, and here that work is the maintainer's own. The other catalogues cannot take
it without misattributing it, and a misattributed reference is the one thing the data cannot afford,
since the reference is what says which catalogue holds a pattern.

`Idioms` is the wrong shelf, and for the reason ADR-0013 gives for it existing. It answers *no work in
particular*; here there is a work, with a title, a date and an author, and the entries read back to it.
Putting them under `Idioms` would discard the citation that makes an entry worth anything — the same
argument ADR-0036 makes for Scoped Locking. ADR-0013's wish to avoid single-entry catalogues is respected
in spirit: this one opens with two patterns and four roles, and is expected to grow, which a catalogue
named for an author can do without the question *which book is this from* ever arising again.

The admission bar stays where ADR-0035 put it. An entry needs a written presentation with a problem and a
solution, because the summary, the roles and the assertions are built out of them; being something the
maintainer happens to use is not enough. That is what keeps the catalogue from becoming a drawer.

The name follows the instrument already used for `GangOfFour` and `Posa2`: the name by which the work is
known to the people who go looking for it. Here the author is the work. This does sit uneasily with
ADR-0038's reason for refusing the vendor name — a package family named after the publisher says nothing
about what is inside — and it is raised under *Risks* rather than argued away: the package is
`DesignPatternCatalog.Reefact`, so it carries the catalogue prefix like all the others, and the word that
follows names an author's body of work rather than a vendor's catalogue of everything.

## Alternatives Considered

### Shelve the four under `Idioms`

Considered because ADR-0013 exists for exactly a pattern with a source and no catalogue, and nothing new
would have to be admitted.

Rejected because the four have a body of work of their own, which is what disqualifies a pattern from
`Idioms`, and because the catalogue would lose the link between a pattern and the article that explains
it.

### Add them to `DomainDrivenDesign`

Considered because they are about value objects, and `ValueObject` lives there.

Rejected because Evans' book does not present them (ADR-0028), and because a relation to `ValueObject`
would still be impossible if they lived in another catalogue (ADR-0027) — a reader would be shown a
proximity the data cannot back.

### One catalogue per article

For example a catalogue for value objects only. Considered because it follows "one package per
catalogued work" literally.

Rejected because the maintainer's patterns do not all arrive as articles about one subject, and a
package for every article would be a package of two attributes. A catalogue of one author's body of work
is the unit that stays useful as it grows.

## Consequences

### Positive

* The four attributes have a place with a citation, a guide page and a worked example.
* The next pattern the maintainer writes up has a place to go and a bar to clear.

### Negative

* The catalogue is open-ended by construction. The word *complete* means nothing for it, as for `Idioms`,
  and the README says so.
* One more package to maintain, with its own public API baseline.

### Risks

* The catalogue becomes a drawer for whatever the maintainer uses. The write-up requirement is the only
  guard, and it is a rule of review rather than something the build enforces.
* ⚠️ **Tension with ADR-0013** (shelve a pattern without a body of work under idioms) **and ADR-0038**
  (name the packages after the catalogue rather than the vendor). Neither is contradicted outright — the
  entries have a body of work, and the package keeps the catalogue prefix — but a maintainer who reads
  ADR-0013's "without inventing single-entry catalogs" as a rule rather than as a reason may disagree.
* An article can be revised. The reference carries the year of first publication, and an entry whose
  article changes underneath it is not noticed by anything.

## Follow-up Actions

* Write the pattern guide for `Hydration` and `CollaborationMethod`, in both languages.
* Decide, when a second author's text is proposed, whether the catalogue stays the maintainer's own.

## References

* [ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.md),
  [ADR-0027](0027-ship-one-independent-package-per-catalogued-work.md),
  [ADR-0028](0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.md),
  [ADR-0035](0035-index-the-pattern-language-and-require-a-write-up.md),
  [ADR-0038](0038-name-the-packages-after-the-catalogue-rather-than-the-vendor.md)
* [ADR-0043](0043-let-a-role-link-to-a-type-that-is-not-a-role.md) — the link `CollaborationMethod` needs
* Reefact, *Advanced Value Objects in .NET*, 2026 — `reefact.net`
