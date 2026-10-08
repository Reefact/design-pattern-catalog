# ADR-0043 | Let a role link to a type that is not a role

🌍 🇬🇧 English (this file) · 🇫🇷 [Français](0043-let-a-role-link-to-a-type-that-is-not-a-role.fr.md)

**Status:** Proposed
**Proposed:** 2026-10-08
**Decision Makers:** Reefact

## Context

A role can declare optional links to other roles of its pattern, each carried by a `Type`
([ADR-0008](0008-bind-participants-with-typed-links.md)). The catalogue format and the generator know
no other kind: a link's name must be the name of a sibling role, the generated property is documented
as pointing at that role's attribute, and a test asserts that every link property of every shipped
attribute names a sibling.

`CollaborationMethod`, the second pattern of the `Reefact` catalogue
([ADR-0042](0042-admit-a-catalogue-for-the-maintainers-own-patterns.md)), marks a member that one named
collaborator may call and nobody else. Its whole content is a type — the collaborator — and that type
is not a participant of the pattern: it is whatever class the author chose, annotated with nothing. The
pattern has one role, so there is no sibling to point at, and no second role would be honest, since
nobody annotates the collaborator with it.

No other entry among the 345 needs this. Until `CollaborationMethod`, the format's one kind of link was
sufficient.

## Decision

A role may declare, beside its links to sibling roles, optional typed links to types that are no role of
its pattern.

## Rationale

The thing to say is a type, and ADR-0008's reasons for carrying a link as a `Type` apply unchanged: the
compiler checks it, refactoring follows it, and it names something that already exists rather than a key
to be kept consistent by hand. A restriction that named its collaborator by string would silently go
stale at the first rename — precisely what ADR-0008 turned down for links between participants.

The capability is used from the day it lands, so
[ADR-0031](0031-carry-no-generator-machinery-for-an-unused-capability.md)'s objection to machinery no
entry exercises does not apply. `CollaborationMethod` is the entry that exercises it.

The links are declared in the catalogue and not inferred, for the reason the catalogue is data
([ADR-0002](0002-keep-the-pattern-catalog-as-data-and-generate-the-attributes.md)): a property that
appears in a generated attribute should be there because the data said so. The test that checks links
accepts a property that names no sibling only when the catalogue declares it, so a template slip cannot
add one without the data.

This complements ADR-0008 rather than replacing it. Its decision — links between roles of a pattern —
stands for every entry that has one; this adds a second kind beside it.

## Alternatives Considered

### A second role standing for the collaborator

Considered because it needs nothing new: a `Collaborator` role, and `CollaborationMethod` linked to it.

Rejected because nobody would ever annotate with it. It would be a role that exists to give a link a
name, it would turn a flat attribute into a nested one (`[CollaborationMethod.CollaborationMethod]`), and the catalogue
would claim a participant the code never declares.

### A positional constructor argument

`[CollaborationMethod(typeof(Price))]`. Considered because it is the shortest form.

Rejected because every link in the catalogue is a named optional property, and a reader of one attribute
should find the same shape in the next. A positional argument is also required, which a link has never
been.

### A string naming the collaborator

Rejected for the reason ADR-0008 rejected it: it is a magic value the compiler does not check.

## Consequences

### Positive

* A role can name a type the pattern does not own, checked by the compiler.
* The format change is small and used immediately.

### Negative

* The catalogue format has two kinds of link, and the index shows both.

### Risks

* A link is optional, so `[CollaborationMethod]` without a collaborator compiles and says only that something is
  restricted. An architecture rule is the place to require the collaborator; the attribute does not.
* This is judged a complement to ADR-0008 and not a supersession. A maintainer who reads it as the latter
  should say so, and the record would be reissued as one.

## Follow-up Actions

* Decide, if another entry needs it, whether an external link may be required.

## References

* [ADR-0008](0008-bind-participants-with-typed-links.md),
  [ADR-0031](0031-carry-no-generator-machinery-for-an-unused-capability.md),
  [ADR-0042](0042-admit-a-catalogue-for-the-maintainers-own-patterns.md)
