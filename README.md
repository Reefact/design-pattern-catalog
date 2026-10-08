# design-pattern-catalog

A vocabulary of .NET attributes that lets code state **which design pattern a type
or a member participates in**.

```csharp
[Composite.Component]
public interface INode { }

[Composite.Leaf(Component = typeof(INode))]
public sealed class FileNode : INode { }

[Composite.Composite(Component = typeof(INode))]
public sealed class FolderNode : INode { }
```

That is the whole of it. The attributes carry no behaviour, hold no dependency and
run no code — they are declarative data, and what you build on top of them is
yours: an inventory, a diagram, an architecture rule, a review checklist.

## Why

A codebase already contains its patterns; what it does not contain is the fact
that it contains them. `OrderRepository` is a repository because of its name, and
`Cache` might be a decorator, a proxy, or neither. The information lives in a
reviewer's head, in a wiki that is out of date, or nowhere.

An annotation puts it in the one place that cannot drift from the code, and makes
it machine-readable on the way — which is what turns "we use a hexagonal
architecture" from a claim into something a build can check.

## What is in it

| Catalog | Patterns | | Source |
|---|---|---|---|
| `GangOfFour` | 23 | complete | Gamma, Helm, Johnson, Vlissides — *Design Patterns*, 1994 |
| `DomainDrivenDesign` | 23 | complete | Evans — *Domain-Driven Design*, 2003 |
| `EnterpriseApplicationArchitecture` | 51 | complete | Fowler — *Patterns of Enterprise Application Architecture*, 2002 |
| `AnalysisPatterns` | 39 | in progress | Fowler — *Analysis Patterns*, 1997 |
| `AccountingPatterns` | 9 | complete | Fowler — *Accounting Patterns*, 2000 |
| `EnterpriseIntegration` | 65 | complete | Hohpe & Woolf — *Enterprise Integration Patterns*, 2003 |
| `XUnitTestPatterns` | 62 | complete | Meszaros — *xUnit Test Patterns*, 2007 |
| `MicroservicesPatterns` | 41 | in progress | Richardson — *Microservices Patterns*, 2018 |
| `Posa2` | 17 | complete | Schmidt, Stal, Rohnert & Buschmann — *Pattern-Oriented Software Architecture, Volume 2*, 2000 |
| `DependencyInjection` | 11 | complete | van Deursen & Seemann — *Dependency Injection Principles, Practices, and Patterns*, 2019 |
| `Idioms` | 2 | open-ended | patterns with a source but no catalog of their own — each entry names its own |

**343 patterns, 619 roles** today, and the catalog is meant to grow by an order of
magnitude. *Complete* means every pattern of the work is either held or named in
[the exclusion tables](catalog/README.md#patterns-deliberately-left-out) with the reason it
cannot be annotated — so in those eight, a missing pattern is a defect rather than work in
progress. A pattern is held by every catalogue whose work presents it as one of its
own, under the name that work gave it — so a reader of a book finds its patterns
spelled as it spelled them, and a work that merely cites another's pattern does not
claim it.

**[Browse the catalog](doc/generated/catalog-index.md)** — every pattern, the
annotation to type for each of its roles, what each role may be applied to, and a
link to its source and to a worked example.

**[Learn the patterns](doc/handwritten/for-users/)** — a separate, hand-written guide
that answers what the index cannot: what a pattern is for, when to reach for it,
**when not to**, and what it costs, with the worked example read line by line. It is
bilingual and it arrives one catalogue at a time. The
[Gang of Four](doc/handwritten/for-users/gang-of-four/README-en.md) is complete, all
twenty-three; so is
[Domain-Driven Design](doc/handwritten/for-users/domain-driven-design/README-en.md);
and so is
[Dependency Injection](doc/handwritten/for-users/dependency-injection/README-en.md),
whose four anti-patterns are where the guide's rule about not inventing is tested
hardest.
[Enterprise Integration Patterns](doc/handwritten/for-users/enterprise-integration/README-en.md)
is under way — the integration styles, the root patterns, the channels, message
construction, routing and transformation, forty-six of sixty-five. It is the largest
catalogue here and the one the guide will take longest to finish.

## Installing

**One package per catalogue.** Take the vocabulary of the works you actually read:

```
dotnet add package DesignPatternCatalog.GangOfFour
dotnet add package DesignPatternCatalog.DomainDrivenDesign
```

Or take all of them at once:

```
dotnet add package DesignPatternCatalog
```

Each catalogue package is named after its row in the table above, and each is
**independent of the others**: nothing in one refers to a pattern of another, so a
codebase that declares domain-driven design does not carry the Gang of Four. They
share one small package, `DesignPatternCatalog.Core`, which holds the base marker a
reader needs to find every annotation whatever mix you installed.

Every package targets `netstandard2.0` through `net8.0`, so it reaches .NET
Framework 4.6.1 and everything after it, and none has a dependency beyond `Core`.

*Nothing is published yet* — the first release is still ahead, and until then the
packages are built from source.

## How an annotation is written

A pattern with several roles is a container, and each role is its own attribute
nested in it:

```csharp
[Visitor.Element]     public interface IExpression { }
[Visitor.AcceptMethod] TResult Accept<TResult>(IExpressionVisitor<TResult> visitor);
```

A pattern with a single role is flat, and reads as the ubiquitous language:

```csharp
[ValueObject]  public readonly record struct ParcelId(string CadastralReference);
[Entity]       public sealed class Parcel { }
```

Two conventions are worth knowing, because nothing enforces them:

* **Annotate the declaration that introduces a role**, never the implementations.
  A role introduced by an interface is annotated on that interface — the type
  graph already says which classes implement it, and annotating each would count
  one role several times.
* **A link is a `Type`**, not a name. `Component = typeof(INode)` binds
  participants of *one* occurrence of a pattern, so a codebase with three
  composites can still be told apart. It is optional, and only needed where the
  type hierarchy does not already say it.

## How it is read back

The library publishes no reader, on purpose: a consumer already holds the
attribute's type, and everything about a pattern is carried by the shape of its
declaration rather than stored a second time. Four rules turn one into the other,
and they are documented on `DesignPatternAttribute` so they travel with the
package:

| | |
|---|---|
| **Catalog** | the **first** namespace segment below the root — the first, so an organisational sub-namespace folds into the catalog it belongs to |
| **Pattern name** | the declaring type; a single-role pattern has no container and carries its own name |
| **Role name** | the attribute type name, without its `Attribute` suffix |
| **Pattern identity** | the type reached by climbing through an abstract base *declared in the same pattern*, stopping at anything else |

Group by the **identity**, never by the pattern name: `Adapter` names one pattern
in Gang of Four and an unrelated one in ports and adapters, and grouping by name
merges them silently.

The sample project carries a working reader — around a hundred lines — that
applies all four. It is meant to be copied and owned, not depended upon.

## One pattern can narrow another

**Specialisation** — the narrower pattern derives from the broader one, so a rule
written for the broader reaches the narrower without naming it. Fowler's row data
gateway narrows his gateway: every one of the first is one of the second, while a
gateway to a message queue is not a row of anything. Both stay countable patterns.

```csharp
[RowDataGateway] public sealed class PersonRow { }   // is a [Gateway] too
```

**A relation never crosses a catalogue.** Each work ships as its own package with no
reference to the others, so the inheritance a cross-catalogue relation would need
cannot exist. Evans' value object and Fowler's are therefore two patterns here, each
in its own package, each in its author's words — and a rule that wants both names
both attributes. That is a deliberate trade: the catalogues stay independent, and
what they have in common is stated in the books rather than asserted by the
compiler.

Whether two entries of **one** catalogue are one pattern is decided by **the
assertions they carry**, never by their names.

## What it deliberately does not do

* No behaviour, no reflection, no runtime cost. An attribute is inert.
* No reader, no analyzer, no rule engine. Those are yours to write, against a
  vocabulary that is stable and checked by the compiler.
* No pattern that cannot be attached to a type, a member or an assembly. A
  `Module` qualifies a namespace, and C# has no namespace-level attribute, so it
  is absent rather than approximated.

## The reasoning

Almost nothing this library decides is defended by the compiler, and the
attributes are generated from a catalog, so a reader of the output cannot tell a
decided trait from an incidental one. The reasoning is kept in the
[ADR base](doc/handwritten/for-maintainers/adr/) — 41 records, English
canonical with a French translation alongside — and that is where to look when a
shape seems arbitrary.

Contributions are welcome: [`CONTRIBUTING.md`](CONTRIBUTING.md) covers the build
and the commit convention, and [`AGENTS.md`](AGENTS.md) states what an agent — or
a contributor — is expected to do without being asked.

## Licence

Apache-2.0.
