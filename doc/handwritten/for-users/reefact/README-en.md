# Reefact — the pattern guide

🌍 🇬🇧 English (this file) · 🇫🇷 [Français](README-fr.md)

*Advanced Value Objects in .NET* — Reefact, 6 October 2026. Two patterns catalogued, four roles, both written
up here.

This catalogue is not a book. It holds the patterns its maintainer uses that no catalogued work names, each
entered with the text that presents it
([ADR-0042](../../for-maintainers/adr/0042-admit-a-catalogue-for-the-maintainers-own-patterns.md)). It is
open-ended, so *complete* means nothing for it: the pages below are what exists, not what is missing.

This guide is not the catalogue index. The
[index](../../../generated/catalog-index.md#reefact) gives the annotation to type, what each role applies to,
and where the sample is; it is generated, complete, and consulted. These pages give what a pattern is for, when
to reach for it, when not to, and what it costs. They are written by hand
([ADR-0040](../../for-maintainers/adr/0040-write-the-pattern-guide-by-hand-in-both-languages.md)).

## The patterns

*Advanced Value Objects in .NET*. Where the model ends, and who may reach inside it.

| Pattern | What it is for |
|---|---|
| [Hydration](Hydration-en.md) | The one way in and the one way out of a value object: rebuilding it from plain values and reducing it back to them. |
| [Restricted To](RestrictedTo-en.md) | A member opened to one named collaborator and to no other caller. |

## What these pages do not do

They do not invent. The article is the maintainer's own, so a page reports **a position rather than a
consensus**, and says so under *Source*. Where the article gives no criterion — for leaving a pattern out, or
for its advantages as a list — the page says that it gives none, and stops.

Both patterns are conventions the article checks with architecture tests; the attributes of this catalogue
check nothing, like every attribute in this repository
([ADR-0004](../../for-maintainers/adr/0004-keep-the-attribute-base-a-pure-marker.md)).
