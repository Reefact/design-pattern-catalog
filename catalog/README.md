# Pattern catalog

The data behind the attributes. One file per pattern, mirroring the layout of
`DesignPatternCatalog.<Catalog>/`, one project per catalogued work:

```
catalog/GangOfFour/Composite.json  ──generate.py──▶  DesignPatternCatalog.GangOfFour/Composite.cs
                                                 └─▶  doc/generated/catalog-index.md
```

Browsing the catalog is what [`doc/generated/catalog-index.md`](../doc/generated/catalog-index.md)
is for: every pattern, what to type to annotate each of its roles, what each role
may be applied to, and a link to its source and its sample. A directory listing
stops being navigable long before the catalog stops growing.

The generated `.cs` files are committed and are what ships. This folder is a
development-time tool: it exists so that the structure of an attribute — base
class, targets, `AllowMultiple`, `Inherited`, the three read properties — is
written once and cannot drift across the catalog. Only the content of a pattern
is authored here.

## Regenerating

```
python3 catalog/generate.py
```

Rewrites every `.cs` from the JSON. Running it on an unchanged catalog must
leave the working tree clean; that round-trip is what keeps the two in step.

## Adding a pattern

Add `catalog/<Catalog>/<Pattern>.json`, regenerate, review the diff.

```json
{
  "catalog": "GangOfFour",
  "name": "Composite",
  "summary": "Composes objects into tree structures to represent part-whole hierarchies, and lets clients treat individual objects and compositions uniformly.",
  "inherited": false,
  "roles": [
    { "name": "Component", "targets": ["Interface", "Class"], "links": [],
      "summary": "Declares the interface shared by the leaves and the composites of the tree." },
    { "name": "Leaf", "targets": ["Class", "Struct"], "links": ["Component"],
      "summary": "A terminal element of the tree: it has no children." }
  ]
}
```

`pattern.schema.json` describes the format and documents every field. Entries
can be checked against it with any JSON Schema tool, which is what makes a
catalog written in bulk reviewable: a missing role or a bad target is a
validation error rather than something to notice by reading.

A role may also carry `externalLinks`: optional typed properties naming a type that is **not** a role of the
pattern — `CollaborationMethod`'s `Collaborator`, for one ([ADR-0043](../doc/handwritten/for-maintainers/adr/0043-let-a-role-link-to-a-type-that-is-not-a-role.md)).
Use `links` for a participant of the same occurrence and `externalLinks` for anything else.

Two rules the schema cannot state on its own, and which are worth checking too:
every name in `links` must be a role of the same pattern, and role names must be
unique within a pattern.

## Patterns deliberately left out

A pattern named by a body of work and absent from its catalog here reads as an
oversight. These are decisions, taken for one of two reasons, and recorded so
that the absence can be told apart from a gap
([ADR-0011](../doc/handwritten/for-maintainers/adr/0011-leave-out-what-cannot-be-annotated.md)).

**Nothing to attach it to.** C# offers no attribute below the assembly and above
the type, and a marker type invented to carry one would put an artefact of this
system into the code it documents.

| Pattern | Work | What it qualifies |
|---|---|---|
| Module | Domain-Driven Design | a namespace |
| Conformist, Customer/Supplier Development, Partnership, Separate Ways | Domain-Driven Design | the relationship *between* two bounded contexts |
| Context Map | Domain-Driven Design | the whole landscape — it is what you draw *from* the annotations |
| Segregated Core, Abstract Core, Highlighted Core, Distillation Document, Domain Vision Statement | Domain-Driven Design | an act of refactoring, or a document; what they produce is already expressible, a distilled core being an assembly annotated `CoreDomain`, and the abstract core of a framework being a role of `PluggableComponentFramework` |
| Guard Clause | — | a shape a method body takes; nothing holds a role in it |
| Monolithic architecture, Microservice architecture | Microservices Patterns | the **application**, which is above the assembly and so has no declaration. They are also what a reader concludes *from* the annotations — the same ground as Context Map |
| Multiple service instances per host, Service instance per host, Service instance per VM, Service instance per Container, Serverless deployment, Service deployment platform | Microservices Patterns | how an artifact is **packaged and run**. One assembly can hold all six over its life without a line changing, so an annotation on it would distinguish nothing |
| 3rd party registration | Microservices Patterns | a registrar **outside** the service — Registrator, Prana, Kubernetes. The pattern's stated benefit is that the service code does none of this, so its participant is by construction not in the codebase |
| Log aggregation | Microservices Patterns | the centralized logging service. What is in the codebase is a logging call, which every codebase has whether or not anything aggregates |
| Cyclic Dependencies | Dependency Injection | a **cycle**, which is a property of a graph rather than of a declaration. Annotating each participant would assert a relation the attribute does not carry, and would say of each class something that is only true of the set |

**Nothing a tool could check.** A role licenses no verifiable assertion, so an
attribute would name it without letting anything range over it — the criterion of
[ADR-0007](../doc/handwritten/for-maintainers/adr/0007-decide-sameness-by-the-assertions-a-pattern-carries.md),
applied to whether a pattern belongs here at all.

| Pattern | Work | Why |
|---|---|---|
| Intention-Revealing Interfaces | Domain-Driven Design | asks that names come from the ubiquitous language; nothing mechanical distinguishes a good name from a bad one |
| Conceptual Contours | Domain-Driven Design | a judgement about where a model's seams fall, not a property of a declaration |
| Ubiquitous Language, Continuous Integration, Evolving Order | Domain-Driven Design | practices of a team, not participants in code |
| Model-Driven Design, Hands-on Modelers, Declarative Design, System Metaphor, Refactoring Toward Deeper Insight, Drawing on Established Formalisms | Domain-Driven Design | ways of working, or of thinking about a model; a codebase can follow all six and no declaration is a participant in any |
| Responsibility Layers | Domain-Driven Design | what the pattern asserts is an **order** — each layer depends only on those beneath it, and the layers are ranked by rate of change — and nothing in this vocabulary orders assemblies. Taking the five Evans names (Potential, Operations, Decision Support, Policy, Commitment) as fixed roles would supply one, but those are the layers he found in a shipping domain, offered as an illustration; the pattern is finding your own |
| Log deployments and changes | Microservices Patterns | a practice of whoever operates the application — *log every deployment and every change to the environment*. No declaration participates, which is the ground that excludes Continuous Integration and Evolving Order |
| Big Ball of Mud | Foote and Yoder, *Pattern Languages of Program Design 4*, 2000 | what it asserts about a participant is that it has no discernible structure, which is the absence of an assertion rather than one. Reached through Evans, who uses it to characterise a neighbouring context, and decided on the same criterion that admits Smart UI ([ADR-0023](../doc/handwritten/for-maintainers/adr/0023-admit-an-anti-pattern-on-the-same-terms-as-any-pattern.md)) |

**Code smells are excluded as a category, and that is a decision rather than a criterion.**
`ConstructorOverInjection` and `AbuseOfAbstractFactories` are annotatable — a constructor and a
factory abstraction — and they do license assertions, so both would pass the two tests above. They are
absent because
[ADR-0037](../doc/handwritten/for-maintainers/adr/0037-admit-the-dependency-injection-catalogue.md)
refuses the **kind**, on the ground that an anti-pattern annotation earns its place as a *baseline* —
the count of what is known and accepted, held by a build at *no more than this* — and a baseline needs
a number that does not move when the reviewer changes. A shape gives one; `ConstructorOverInjection`'s
*too many* does not.

`AbuseOfAbstractFactories` is the borderline case and it is worth naming as one: it is a shape rather
than a quantity, so the argument does not really reach it. It goes out with the other two because the
decision is about the kind — a rule the next contributor can apply without reopening the record — and
that record's *Alternatives Considered* carries the one-line amendment that would let it back in.

**Anti-patterns are not excluded as a category.** `SmartUi` is catalogued, because
Evans names it, a class or an assembly holds it, and it licenses assertions — the
usual three. It is the only entry whose assertions *exempt* rather than constrain,
and [ADR-0023](../doc/handwritten/for-maintainers/adr/0023-admit-an-anti-pattern-on-the-same-terms-as-any-pattern.md)
records why that is admitted rather than special-cased.

## How complete each catalogue is

A count on its own does not say whether a catalogue is finished. Twenty-three Gang of Four
patterns is the whole book; thirty-nine *Analysis Patterns* is where somebody stopped. Until
this was written down the two looked the same, and an absent pattern could not be told from a
deliberate one — which is the condition
[ADR-0001](../doc/handwritten/for-maintainers/adr/0001-check-every-pull-request-against-the-adr-base.md)
exists to prevent, applied to catalogues rather than to decisions.

| Catalogue | Held | Its work | Status |
|---|---|---|---|
| `GangOfFour` | 23 | 23 | **complete** — every pattern of the book |
| `EnterpriseApplicationArchitecture` | 51 | 51 | **complete** — checked name by name against Fowler's own index at `martinfowler.com/eaaCatalog` |
| `AccountingPatterns` | 9 | 9 | **complete** — the whole of the 2000 paper |
| `EnterpriseIntegration` | 65 | 65 | **complete** |
| `XUnitTestPatterns` | 62 | 68 | **complete** — the other six are in the exclusion tables above |
| `DomainDrivenDesign` | 23 | 45 + 2 | **complete** — with one open question about a possible twenty-fourth entry, below |
| `MicroservicesPatterns` | 41 | 51 | **read whole** — 41 held, 11 excluded in the tables above, 1 in the held-back section, and around half the work will be excluded ([ADR-0033](../doc/handwritten/for-maintainers/adr/0033-admit-microservices-patterns-as-a-catalogue.md)) |
| `Posa2` | 17 | 17 | **complete** — all four chapters that hold patterns, admitted by [ADR-0036](../doc/handwritten/for-maintainers/adr/0036-admit-posa2-as-a-catalogue.md) |
| `DependencyInjection` | 11 | 14 | **complete** — the eleven [ADR-0037](../doc/handwritten/for-maintainers/adr/0037-admit-the-dependency-injection-catalogue.md) admits. Chapter 6's three are refused, one on ADR-0011 and two by decision, and four concepts named outside the catalogue sections are an open question below |
| `Reefact` | 2 | — | **open-ended by construction** — the maintainer's own patterns, each entered with the text that presents it ([ADR-0042](../doc/handwritten/for-maintainers/adr/0042-admit-a-catalogue-for-the-maintainers-own-patterns.md), proposed) |
| `AnalysisPatterns` | 39 | — | **deliberately stopped**, and the only one that is |
| `Idioms` | 2 | — | **never complete by construction** ([ADR-0013](../doc/handwritten/for-maintainers/adr/0013-shelve-a-pattern-without-a-body-of-work-under-idioms.md)) |

In all eight marked complete, a pattern of the work that is neither catalogued nor named in an
exclusion table above is a **defect**, not work in progress. That is what the word is for here.
The open question below is about whether one *more* entry belongs, not about a gap.

**Domain-Driven Design, counted against Evans' own reference.** The *DDD Reference* he
publishes under Creative Commons lists **45** patterns; the catalogue holds 21 of them, 19 are
in the exclusion tables, and two more entries — `Specification` and `SmartUi` — come from the
2004 book without appearing in the reference's contents, which is why the total is 23 rather
than 21. Checking the two lists against each other turned up four things worth fixing and one
worth asking:

* **Two exclusions were spelled in this file's words rather than in Evans'.** *Hands-On
  Modellers* is his *Hands-on Modelers*, and *Customer/Supplier* is his *Customer/Supplier
  Development*. A work's own spelling is what an entry carries
  ([ADR-0028](../doc/handwritten/for-maintainers/adr/0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.md)),
  and an exclusion is no different — a reader searching for the name Evans used found nothing.
* **Two patterns were in neither list.** *Refactoring Toward Deeper Insight* and *Drawing on
  Established Formalisms* are ways of working, so they belong with the other four in the
  practices row; they were simply never written down.
* **`KnowledgeLevel` is the open question, and it is the maintainer's.** It is catalogued under
  `AnalysisPatterns`, where Fowler named it. Evans gives it a section of his own reference, in
  his own pattern language — which reads as a presentation under ADR-0028, and would make it
  the third name held by two catalogues, beside `Repository` and `ValueObject`. But ADR-0024
  described it as reached "through Evans, who sends the reader to Fowler for it", which reads
  as crediting rather than presenting. **The two readings are not settled by anything read
  here**, so nothing was changed: deciding it needs the 2004 book's own words, not a
  recollection of them.

**Analysis Patterns is the one catalogue stopped on purpose**, and stopping is a decision like
any other. Chapters 2, 3, 4, 5 and 8 are catalogued; chapter 6 is superseded by the accounting
paper
([ADR-0026](../doc/handwritten/for-maintainers/adr/0026-follow-an-authors-own-supersession-of-a-catalogued-chapter.md));
the rest is untouched. A reader counting thirty-nine against the book should read it as work
paused rather than a catalogue with holes.

## Chapters catalogued whole, including what a contents page does not name

Chapter 2 of *Analysis Patterns* is complete: its nine sections are catalogued, and
so are two patterns the section titles do not name. **Chapters 3 and 5 are complete
too** — twelve sections and four, every one of which held up against the criteria,
which is not something to assume of the chapters still to come: chapter 7 is a worked
example whose sections are steps rather than patterns, and most of chapter 11
qualifies a package, which C# gives nothing to annotate.

**Chapter 4 is complete at four of its five sections.** Enterprise Segment,
Measurement Protocol, Range and Phenomenon with Range are catalogued; §4.5 *Using the
Resulting Framework* is not, because it applies the four rather than adding a fifth —
the same shape as chapter 7, and the reason to say so here is that a reader counting
sections against entries would otherwise find one missing. `StatusType` is a fifth
entry from §4.2.3, which names it; it earns its own entry rather than roles on the
protocol because what it asserts is about an observation's claim on the world, and a
comparative status is itself observable.

Three things about this chapter are worth recording rather than leaving to be found
again. The chapter's figures spell one method *Casual Calculation*; the contents page
has **Causal**, which is what it is, so that is the spelling the role carries.
`Projection` and `AssociativeFunction` are not new here — chapter 3 already holds them
on `ActiveObservation` and `AssociatedObservation` — so figures 4.9 and 4.24 add only
`Plan` and the range function. And the UML companion redraws sixteen of the chapter's
twenty-four figures: 4.2, 4.6, 4.13–4.16, 4.18 and 4.23 are absent, and 4.13–4.16 fall
in *Creating a Measurement*, which is procedural. The entries rest on the sixteen.

Chapter 5 is worth a note of its own because its four entries are about *identity*,
and three of them are distinguished from one another only by what they permit.
`Name` permits several and permits none. `IdentificationScheme` permits several and
scopes uniqueness to an issuer. `ObjectMerge` asserts sameness on the system's own
authority; `ObjectEquivalence` records who asserts it and so admits disagreement —
which is the difference between a duplicate cleaned up and two catalogues that do
not concur.

**Chapter 8 is complete: all seven sections.** Proposed and Implemented Action,
Completed and Abandoned Actions, Suspension, Plan, Resource Allocation, Outcome and
Start Functions — and its Protocol, catalogued under another name for the reason below.
Its UML companion redraws all seventeen figures, so nothing here rests on inference.

Two departures from the naming convention below are worth stating here rather than
leaving to be noticed.

Section 3.10 is titled *Active Observation, Hypothesis, and Projection*; its faithful
PascalCase is unreadable, so the entry is `ActiveObservation` and the other two are
roles of it.

Section 8.5 is titled *Protocol*, and `AnalysisPatterns/Protocol` was already taken by
chapter 3. **They are two patterns, not one spelled twice.** Chapter 3's records the
method by which an observation was made, so that two results of one phenomenon type
obtained differently are not interchangeable — which is why `MeasurementProtocol`
narrows it. Chapter 8's is a composite of steps at the knowledge level whose operational
instance is a plan (figures 8.9, 8.10 and 8.12). Different assertions, so
[ADR-0007](../doc/handwritten/for-maintainers/adr/0007-decide-sameness-by-the-assertions-a-pattern-carries.md)
makes them two entries — and since one catalogue cannot hold the name twice, chapter 8's
is `PlanProtocol`, named after what it is the knowledge level *of*.

Both are judgements against the rule, taken because the rule produced an unusable or an
impossible name, and both are the kind of thing a maintainer may reverse.

`Leveled Accountability Type` and `Directional Accountability Type` appear only in
figures 2.12 and 2.13, as «overlapping» siblings of the hierarchic one. They meet
the three criteria like any other entry — the work names them, a class holds them,
they license assertions — so the only question was whether a name given in a
diagram is *the name the work gave it* under
[ADR-0006](../doc/handwritten/for-maintainers/adr/0006-catalogue-a-pattern-where-the-work-that-named-it-put-it.md).
It is: the rule is about which work names a pattern, not about which part of the
work. So the convention this chapter sets is **the section title where the book has
one, the diagram's class name where it does not** — which is why
`HierarchicAccountability` carries the section-2.7 spelling while its two siblings
carry theirs from the figures.

Three entries were resolved rather than catalogued as they stood, and how they were
resolved is worth recording because each turned on a comparison rather than on a
judgement:

| Pattern | How it was settled |
|---|---|
| Party Type Generalizations | **An entry of its own.** Figure 2.10 asserts what `KnowledgeLevel` does not: a supertype / subtypes hierarchy on *Party Type* itself, plus a derived closure that the accountability type's constraint ranges over instead of the immediate type |
| Organization Structure | **A specialisation of `Accountability`.** Figures 2.6 and 2.7 are drawn as 2.8 is, with *organization* for *party* and *parent* / *subsidiary* for *commissioner* / *responsible*. Restricting both ends to organizations is an added assertion, so it is narrower rather than the same thing spelled differently — [ADR-0007](../doc/handwritten/for-maintainers/adr/0007-decide-sameness-by-the-assertions-a-pattern-carries.md) |
| Organization Hierarchies | **An entry of its own, and not that one.** Figure 2.4 has *no type object at all* — the admissible nesting is an invariant on each subtype — and figure 2.5 is Fowler showing why that collapses once a second structure appears. What it asserts is that one parent suffices, which is a claim about a participant and not merely a smaller version of the structure pattern |
## When the author says a chapter is superseded

The UML companion Fowler publishes for chapter 6 of *Analysis Patterns* carries a note
in his own hand: a more up-to-date discussion of accounting patterns is at
`martinfowler.com/apsupp/accounting.pdf`, and the patterns there supersede the book's.
The note is on that chapter's companion and on no other.

So **chapter 6 is not catalogued from the book**, and the paper — *Accounting Patterns*,
seventy-two pages, its PDF created 8 December 2000 — is catalogued as
`AccountingPatterns` instead. The decision is
[ADR-0026](../doc/handwritten/for-maintainers/adr/0026-follow-an-authors-own-supersession-of-a-catalogued-chapter.md),
and its argument is that a rule protecting a work's authorship should not be turned
against the author himself: replacing one's own model is not a rival presentation of it.

The paper has **nine patterns**, read from its own section headings: Event (p11),
Accounting Entry (p15), Posting Rule (p19), Secondary Posting Rule (p33), Account (p39),
Accounting Transaction (p44), Reversal Adjustment (p53), Difference Adjustment (p59) and
Replacement Adjustment (p69).

### What became of chapter 6's fifteen sections

| Book section | In the paper |
|---|---|
| Account | **`Account`** — and the paper takes the entries *out* of it. Fowler says so in the text: "Account often goes with Accounting Entry. Indeed in *Analysis Patterns* I put them in the same pattern" |
| Transactions | **`AccountingTransaction`**, with the sum-to-zero invariant stated, and two-legged and multi-legged as separate roles |
| Posting Rules | **`PostingRule`**, with the host — a service agreement, a business unit — made a role, which is what carries "different rules for different business units" |
| Posting Rule Execution · Posting Rules for Many Accounts | folded into `PostingRule` and `SecondaryPostingRule` rather than kept as patterns of their own |
| Individual Instance Method · Summary Account · Memo Account · Choosing Entries · Accounting Practice · Sources of an Entry · Balance Sheet and Income Statement · Corresponding Account · Specialized Account Model · Booking Entries to Multiple Accounts | **no pattern of their own in the paper** |

The last row is the honest state of it, and it is where a maintainer's eye is wanted.
ADR-0026 records the risk in its own words: a book pattern with no successor is absent
for a reason that is *not* supersession, and whether any of those ten should be
catalogued from the book despite the note is not a question this file can settle.

Three of the paper's nine have no section in chapter 6 at all — `Event`, and the pair of
adjustments beyond the reversal. The paper is built around reacting to an event, which
is the shift the note is really about.

### The three adjustments are siblings

The three adjustments are siblings and not a hierarchy. Each is a whole strategy for one
problem — you cannot edit a booked entry — and they differ in what they cost:
`ReversalAdjustment` keeps everything and pays in entries, `DifferenceAdjustment` pays
one entry and loses the statement of what the figure should have been, and
`ReplacementAdjustment` trades the audit trail away on purpose.

## Enterprise Integration Patterns, and what a channel's annotation depends on

**All sixty-five are catalogued.** The integration styles, the base patterns, the channels,
message routing, message construction, message transformation, the messaging endpoints and
system management — the whole book, in its own order but for routing, which was taken
before construction and is the one detour recorded below.

It is the largest catalogue here and the first taken to completion, which changes what an
absence means: a pattern of this book that is missing is now a defect rather than work in
progress.

**Routing was taken before construction**, and construction closed the gap that left.
Routing went first because it is the core of the work — the router, the splitter, the
aggregator and the process manager are what a messaging codebase is made of, while
message construction is mostly properties on a message. Chapter 5 was then filled behind
chapter 7. The detour is recorded because it happened, and because a reader comparing the
commit history to the book would otherwise take it for a gap.

**A pattern the book builds out of other patterns gets one role, not a role per part.**
`ComposedMessageProcessor` is a splitter, a router and an aggregator; `Normalizer` is a
router and a translator per format. In both the entry names the assembled whole, and the
parts inside wear `Splitter`, `MessageRouter`, `MessageTranslator` and the rest
themselves. Giving a composite a role per constituent would count the same participant
twice — once under its own pattern, once under the composite — and a codebase with three
normalizers could no longer say how many translators it has.

Its admission is
[ADR-0029](../doc/handwritten/for-maintainers/adr/0029-admit-enterprise-integration-patterns-as-a-catalogue.md),
which also settled the two judgements this work forces.

**The channels are in, and their annotation depends on the codebase.** A channel is often a
configured queue name rather than a type, and where that is so there is nothing to annotate
— the pattern is simply not used, which is the ordinary condition of every role rather than
a defect in the entry. Where a codebase has a typed abstraction per channel, and that is
common in .NET, the role attaches to it. They are catalogued because the routing patterns
route *between* channels and the endpoint patterns consume *from* them: a catalogue without
channels describes half a mechanism, and an absence with no record reads as an oversight.

**Four relations, and around thirty deliberately not.** The book states a family in two
ways, and only one of them is carried
([ADR-0030](../doc/handwritten/for-maintainers/adr/0030-relate-only-the-narrowings-a-work-states-outright.md)).

| What the book does | Here |
|---|---|
| states a `WireTap` **is** a fixed `RecipientList` with two output channels | `specialisationOf` |
| presents `CommandMessage`, `DocumentMessage` and `EventMessage` as three kinds of `Message` | `specialisationOf` |
| prints the twelve routing patterns under `MessageRouter` | unrelated |
| prints the six transformation patterns under `MessageTranslator` | unrelated |
| prints the channels under `MessageChannel`, the consumers under `MessageEndpoint` | unrelated |

The test is
[ADR-0007](../doc/handwritten/for-maintainers/adr/0007-decide-sameness-by-the-assertions-a-pattern-carries.md)'s:
a sentence saying one pattern *is* another is an assertion the author made; a chapter heading
is neighbourhood. Twelve patterns are printed under `MessageRouter` because they are about
routing, and reading each as a message router is reading the table of contents rather than
the text.

The four are emitted at the precision the relation has —
`WireTapAttribute : RecipientList.Role`, so a wire tap answers as *a participant in* a
recipient list rather than as the recipient list itself. That is what the six relations of
this shape in the other catalogues say too. A codebase that wants the precise role writes
both attributes.

An earlier version of this file gave a different reason for leaving the three message
intents unrelated: that the relation would assert something the book does not. **That was
wrong** — it under-specifies, it does not misstate — and it is what sent the question to an
ADR.

**`CompetingConsumers` keeps a plural name for a role that annotates one class**, and that
is deliberate. It is the name the book gives, and the rule for names is to spell a pattern
as its work spelled it
([ADR-0028](../doc/handwritten/for-maintainers/adr/0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.md)).
Reading `[CompetingConsumers]` on one consumer is also true to the pattern: a single
competing consumer is not one, the arrangement is, and the plural is what stops a reader
taking the annotation for a property of the class instead of a statement about the channel
it shares.

**Pipes and Filters and Message Broker are held here although POSA named them first** in
1996. The test is
[ADR-0028](../doc/handwritten/for-maintainers/adr/0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.md)'s:
this work names each, describes it in full and gives it a place in its own pattern language,
which is a presentation. Crediting an earlier source is scholarship, not the passing mention
that rule excludes. If POSA is ever catalogued it holds its own entries and neither
catalogue refers to the other.

### Three homonyms, expected and unrelated

This work carries three names the catalogue already holds elsewhere. All three are now
here. They are **different patterns**, and since each catalogue ships as its own package
nothing in the packages says so — hence this table.

| Here | Already held as | Why they are not the same |
|---|---|---|
| `EnterpriseIntegration/MessagingGateway` | `EnterpriseApplicationArchitecture/Gateway` | Fowler's wraps any external resource behind a simple interface; this one hides a messaging API from application code |
| `EnterpriseIntegration/MessagingMapper` | `EnterpriseApplicationArchitecture/Mapper` | Fowler's moves data between two objects that should not know each other; this one moves it between a domain object and a message |
| `EnterpriseIntegration/SmartProxy` | `GangOfFour/Proxy` | the Gang of Four's stands in for an object; this one intercepts a request and its reply in order to observe them |

Three days ago each would have been a question of which publication held the definition.
Since [ADR-0027](../doc/handwritten/for-maintainers/adr/0027-ship-one-independent-package-per-catalogued-work.md)
made the catalogues independent, there is nothing to arbitrate — only this note to write.

## xUnit Test Patterns, and the five words nobody agrees on

**The book is complete.** Sixty-two of its sixty-eight patterns are catalogued and the other
six are left out on purpose, each with its reason in the table above — nothing in this work is
now unaccounted for.

That changes what an absence means here, as it did for *Enterprise Integration Patterns*: a
pattern of this book that is neither catalogued nor listed as an exclusion is a defect rather
than work in progress. Its admission is
[ADR-0032](../doc/handwritten/for-maintainers/adr/0032-admit-xunit-test-patterns-as-a-catalogue.md).
A reader counting sixteen against sixty-eight is looking at work in progress, and at a book
about a third of which will not be catalogued at all — roughly ten entries are shapes a
method body takes rather than participants a declaration holds, and every exclusion will be
listed here as it is decided.

**Where each part was read from.** The author's canonical index at `xunitpatterns.com` is
refused by the environment this catalogue is written in, so the pattern list comes from the
publisher's table of contents. Chapter 23 was written from the publisher's free sample
chapter — Meszaros' own problem and solution statements. **Chapter 24 was not**: its names
and page numbers are verified against the publisher's index, and its summaries are written
from knowledge of the patterns rather than from the text in front of the writer. Nothing in
them is asserted about what the book says. The distinction is recorded because a reader
weighing an entry deserves to know which kind it is, and because the two are otherwise
indistinguishable.

**Five kinds and one umbrella, and the distinction is the whole point.** These are the words
a codebase gets wrong most reliably: "mock" is what most people call all five. The entries
carry what separates them, and each is a rule a review can hold to.

| Kind | What it does | What it never does |
|---|---|---|
| `TestStub` | feeds indirect inputs | get consulted afterwards |
| `TestSpy` | records the calls it got | judge them |
| `MockObject` | carries expectations and judges | wait for the test to ask |
| `FakeObject` | works, lightly | stay in production |
| `ConfigurableTestDouble` | is told what to answer at run time | come pre-decided |
| `HardCodedTestDouble` | has its answer written in | be told anything |

A stub that has grown a `VerifyWasCalled` is a mock wearing the wrong name; a fake is the
only kind with behaviour of its own, so it is the only kind that can be wrong while every
test using it passes.

**Six of the eight narrow `TestDouble`, and one does not.** The relations are the four kinds
plus the two implementation styles, all stated outright by the book —
[ADR-0030](../doc/handwritten/for-maintainers/adr/0030-relate-only-the-narrowings-a-work-states-outright.md)'s
test. Because `TestDouble` has a single role, they emit at full precision:
`TestStubAttribute : TestDoubleAttribute`, so a rule asking for every stand-in in a test tree
reaches all six without naming them.

`TestSpecificSubclass` carries **no** relation although the book prints it in the same
chapter. Its problem statement is *how can we make code testable when we need to access
private state of the SUT*, and its solution subclasses the system under test — it does not
replace a depended-on component, so it is not a double. That is the distinction a reader most
often gets wrong, and it is the one place in this chapter where the chapter heading and the
text disagree.

**The depended-on component is not a role.** Every diagram in the chapter names the DOC — the
thing the double stands in for — and it is deliberately not annotated: it is an ordinary
production type that happens to be replaced in a test, and annotating every interface a test
fakes would annotate most of a codebase without asserting anything about it.

**The roles are `inherited`.** A subclass of a fake is still a fake, unlike a subtype of a
Gang of Four Component. That is a property of these patterns rather than a default: what
makes a class a double is what it stands in for, and deriving from one does not stop it
standing in.

**The three organisations are the point of chapter 24.** `TestcaseClassPerClass`,
`TestcaseClassPerFeature` and `TestcaseClassPerFixture` are mutually exclusive answers to
one question — what does a testcase class correspond to — and a test tree usually holds all
three without anyone having decided. Each survives a different change: per class follows a
refactoring of the production tree, per feature survives one, per fixture keeps a setup that
is true for every test that reads it.

`TestcaseSuperclass` and `TestHelper` are the same pairing for sharing code: inheritance
against delegation. The superclass spends the one base class a testcase class has and hides
the setup in a parent; the helper relates nothing to anything. Which was chosen is invisible
in the code and is exactly what an annotation is for.

**Chapter 24's roles are not `inherited`, and chapter 23's are.** A subclass of a fake is
still a fake — what makes a double a double is what it stands in for, and deriving from one
does not stop it standing in. A subclass of a testcase superclass is a testcase class and not
a superclass: an organisation is a decision about one declaration, not a nature a subtype
carries. The flag is a fact about each pattern rather than a default
([ADR-0009](../doc/handwritten/for-maintainers/adr/0009-let-each-role-declare-what-it-applies-to.md)).

**The three organisations narrow `TestcaseClass`**, which chapter 19 brought. The book
presents them as kinds of testcase class, so
[ADR-0030](../doc/handwritten/for-maintainers/adr/0030-relate-only-the-narrowings-a-work-states-outright.md)
carries it. `TestcaseClass` has a single role, so the relations emit at full precision —
`TestcaseClassPerClassAttribute : TestcaseClassAttribute` — and a rule asking for every
testcase class reaches all three organisations without naming them.

Note that the four attributes disagree about `Inherited`, on purpose. A subclass holding
tests is a testcase class, so that role is inherited; a subclass of a class organised per
fixture is not itself organised per fixture, so those three are not. Nothing forces a
narrowing to agree with what it narrows, and here the difference is the point: one is a
nature, the others are decisions about one declaration.

**Chapter 19 is the vocabulary the rest of the book is written in** — test method, testcase
class, assertion method, runner, suite — and most of it is what a framework already gives a
team. Annotating a `[TestMethod]` that xUnit already marks says little; the entries earn
their place elsewhere, where a team built its own. The samples are written for that case: a
runner for a handheld the crane drivers carry, a suite object it composes, and a discovery
rule by naming convention with the gap such rules always have.

**Discovery and enumeration are opposites worth annotating together.** Discovery runs
whatever exists, so its failure is a test written outside the convention and never run.
Enumeration runs exactly what is listed, so its failure is a test written and never added.
A codebase usually has both, in different corners, and which corner is which is invisible.

**Two of chapter 19's eleven are left out**, on the same ground as Guard Clause: they are
shapes a method body takes rather than participants a declaration holds.

| Pattern | Why |
|---|---|
| Four-Phase Test | the arrangement of setup, exercise, verify and teardown *inside* one test method; nothing holds a role in it |
| Assertion Message | the string handed to an assertion — an argument value, not a declaration |

**Chapter 18 is four pairs of opposites, and that is why it is worth annotating.** None of
its ten entries describes a mechanism; each states a choice, and in every case the two
answers are indistinguishable in code.

| Axis | One answer | The other |
|---|---|---|
| how the test was produced | `RecordedTest` | `ScriptedTest` |
| where its cases come from | `DataDrivenTest` | a test whose cases are written in it |
| how much the fixture holds | `MinimalFixture` | `StandardFixture` |
| how long the fixture lives | `FreshFixture` | `SharedFixture` |

The two fixture axes are **orthogonal**: a fixture is minimal or standard *and* fresh or
shared, so one declaration legitimately carries two of these attributes. That is not a
duplication to clean up.

**No relation was added.** The book presents these as strategies rather than as kinds of one
another, and the fixture entries would want a `Fixture` pattern to narrow, which this work
does not have — ADR-0030's test is a sentence about two patterns, and there is none here.

**`BackDoorManipulation` is the entry a codebase most benefits from finding.** Every back
door is a second definition of the data's shape, so when the system's own writing changes,
the back door keeps working and keeps being wrong. Annotating them is what turns "how many
do we have" from an archaeology exercise into a query.

**Chapter 20 is five answers to one question: where does the fixture get built?** Delegated
setup puts it in methods the test calls; implicit setup puts it in the method the framework
calls; lazy setup builds it on first use; suite fixture setup builds it once for a suite; a
prebuilt fixture was there before the run began. A test class usually mixes several without
anybody having chosen, and the choice is invisible: all five leave a test body that says
nothing about where its state came from.

**`ChainedTests` is annotated because it is a hazard, not because it is a recommendation.**
The book offers it as a last resort. It breaks when a runner changes order, parallelises, or
runs one test alone — three things nobody announces — and nothing else in the code admits it
was chosen rather than drifted into. This is the same reason `BackDoorManipulation` is here.

**`CreationMethod` and `Idioms/ObjectMother` are the same idea one level apart**, and nothing
in the packages says so. An object mother is a class of creation methods; Meszaros catalogues
the method, Schuh and Punke named the class. They live in different packages and no relation
crosses a catalogue
([ADR-0027](../doc/handwritten/for-maintainers/adr/0027-ship-one-independent-package-per-catalogued-work.md)),
so a codebase that means both writes both.

**One of chapter 20's nine is left out**, on the ground already used twice:

| Pattern | Why |
|---|---|
| In-line Setup | the fixture built in the body of the test method itself; nothing holds a role in it |

**Chapter 21 is one more pair of opposites, and it is the one the test doubles serve.** State
verification asks the system what it holds afterwards; behaviour verification asks a
collaborator what it was told. The first survives a refactoring that changes the calls and
cannot catch an effect that leaves no trace; the second catches exactly that and breaks when
the delegation changes. `TestSpy` and `MockObject` exist to make the second possible, which is
why the two chapters are worth reading together.

**`UnfinishedTestAssertion` attaches to the test, not to the assertion inside it.** The
assertion is a call, and a call holds no role; what is being stated is that this *test* is a
placeholder. It is also the one annotation in this catalogue whose value is that somebody
comes back and removes it.

**No relation was added, and one is pending.** `CustomAssertion`, `DeltaAssertion` and
`UnfinishedTestAssertion` are all assertion methods, and chapter 19's `AssertionMethod` is
catalogued — but
[ADR-0030](../doc/handwritten/for-maintainers/adr/0030-relate-only-the-narrowings-a-work-states-outright.md)
carries a narrowing the *work states*, and the sentence that would state it has not been read:
this chapter is not among the publisher's free samples. The relation is left unwritten rather
than inferred from the fact that it is probably true. It is the first time that rule has
refused something, and refusing is what it is for.

**One of chapter 21's six is left out:**

| Pattern | Why |
|---|---|
| Guard Assertion | an assertion used *in a guarding position* early in a test; the same method is a guard in one test and an ordinary assertion in another, so no declaration holds the role — the assertion counterpart of Guard Clause, excluded on the same ground |

**Chapter 22 completes the symmetry chapter 20 started, exclusion included.** Setup and
teardown each offer the same three places to put the work — in the test, in a method the
framework calls, or in something that does it for you — and in each chapter the in-line
answer is left out on Guard Clause's ground. What is catalogued is the choice a declaration
can hold.

`GarbageCollectedTeardown` is the odd one and the most useful of the three: it annotates a
fixture that has *nothing* to clean up, which turns an empty tearDown somebody wrote out of
habit into a statement — everything here is reclaimed by the runtime, so no file, no socket,
no row survives the test. The day one does, that is the claim that was broken.

Two more teardowns arrived with chapter 25: table truncation and transaction rollback are
teardown patterns the book files under Database rather than here. They answer a different
question from these three — *what* is undone rather than *where* the undoing is written — so
neither narrows anything catalogued here.

**One of chapter 22's four is left out:**

| Pattern | Why |
|---|---|
| In-line Teardown | the cleaning up written in the body of the test method itself; nothing holds a role in it — the same ground as In-line Setup |
| Literal Value | a value written inline in a test — an expression, not a declaration. A named constant is a different thing: what this pattern describes is precisely the value that is *not* given a name |

**Chapter 25 is the only one whose patterns are about something outside the code**, and every
entry earns its place the same way: what it states is invisible to every measurement the
application makes of itself.

A `StoredProcedureTest` covers logic no code-coverage tool will ever look at, so an
unannotated procedure and an untested one are indistinguishable. A `DatabaseSandbox` is a
thing nobody notices is missing until two runs collide. And the two teardowns carry the
sharper trades: truncation is fast and total, so it will empty a table a colleague's fixture
relied on just as happily; rollback is clean and carries a rule nothing enforces — the system
under test must not commit on its own, so it cannot test anything whose behaviour depends on a
commit, and the failure when it does arrives looking like flakiness.

**All four of the chapter are catalogued**, the first chapter of this work with no exclusion
at all.

**`DependencyInjection` and `HumbleObject` are held here although Fowler and Feathers are the
names attached to them**, and the question is settled by the test that already settled Pipes
and Filters
([ADR-0028](../doc/handwritten/for-maintainers/adr/0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.md)):
does this work *present* the pattern as one of its own? Chapter 26 gives Dependency Injection
eight pages, Dependency Lookup nine, Humble Object fourteen and Test Hook four, each a numbered
pattern in Part III with its own problem statement and its own place in the book's pattern
language. That is a presentation. Crediting an earlier source is scholarship, not the passing
mention the rule excludes.

Nothing collides, either: none of the four names is held by another catalogue today. If
Fowler's *Dependency Injection* is ever catalogued it takes its own entry, in its own package,
and neither refers to the other — which is
[ADR-0027](../doc/handwritten/for-maintainers/adr/0027-ship-one-independent-package-per-catalogued-work.md),
not a judgement to make again.

**Injection and lookup are the chapter's pair of opposites** — how does a participant come by
its collaborators, given from outside or fetched from a registry. The trade is where the
substitution lives: a constructor argument is in the signature, a registry entry is in no
signature at all, so a test that fails because somebody forgot to reset the registry fails a
long way from its cause.

**`TestHook` is the entry to count rather than to admire.** It is production code shipped for
the benefit of a test, offered by the book as a last resort — and a codebase that cannot list
its test hooks has no way to know how many it carries.

**All four of the chapter are catalogued**, the second chapter running with no exclusion.

**`DummyObject` is a sixth test double, filed by the book under the value patterns.** It
narrows `TestDouble` like the five in chapter 23, so a rule asking for every stand-in in a test
tree finds it — which it would not, if the catalogue had followed the chapter it is printed in.

The evidence for that relation is worth naming, because it is weaker than chapter 23's and
stronger than what
[ADR-0030](../doc/handwritten/for-maintainers/adr/0030-relate-only-the-narrowings-a-work-states-outright.md)
refused in chapter 21. Chapter 23 was read from the publisher's free sample. This one rests on
Fowler's *Test Double* page, which reports Meszaros' own taxonomy and names the five kinds
outright — dummy among them. A named source reporting the author's list is not the book, and it
is not an inference either.

**Chapter 27 is about where a value in a test comes from**, and the three answers differ in
what they cost. A derived value states the relationship a hard-coded expectation hides — two
numbers that agree tell a reader nothing about why. A generated value removes collisions
between runs and buys them back as irreproducibility, so a failure that depends on what was
generated cannot be re-run unless what was generated is reported. And a dummy is the value that
is never looked at, which is why the honest implementation throws.

## Microservices Patterns, and the words this catalogue already knew

**Forty-one held, eleven excluded, one waiting — out of fifty-one.** Richardson's pattern
language is indexed at `microservices.io/patterns/index.html`, and the index carries **53 bullets
over 51 distinct pages in 15 groups**: two pages are listed twice, under *External API* and under
*Testing*. Every group has now been read. Its admission is
[ADR-0033](../doc/handwritten/for-maintainers/adr/0033-admit-microservices-patterns-as-a-catalogue.md),
which also estimates that between twenty-five and thirty of the 48 will be admissible: roughly
half the language is deployment and observability topology, which no C# declaration holds.
**The figure this file carried for eight instalments — 48 patterns in fourteen groups — was
wrong.** It came from the admission check and was never recounted. Recounting bullet by bullet
gives 53 over 51 pages in 15 groups, and it turned up a group nobody had looked at:
*Architectural style*, whose two entries were neither catalogued nor excluded. They are excluded
now, above. ADR-0033 carries the old figure and its per-group counts; the numbers here are the
ones to trust.

**Where these entries were read from.** All fifty-one pattern pages were fetched and read —
context, problem, solution, related patterns — so the roles below are the participants the
author names, not participants recalled from the book. Where a page names a thing without
giving it a noun, the name here is this catalogue's and is flagged as such: `ViewUpdater` is
the only one so far, for what the CQRS page calls *the application keeping the database up to
date by subscribing to domain events*. The four roles of `TransactionalOutbox` are the author's
own list.

The work in the `reference` field is the 2018 book, not the site; the site is the same pattern
language maintained by the same author. **Ten of the thirty-eight pages behind a catalogued entry
point at the book in their body.** Seven say outright that it "describes this pattern in a lot more detail"; Saga sends the
reader to section 4.3, Messaging to the book's treatment of inter-communication, and Strangler
application to chapter 13 for the refactoring rather than for the pattern. The other twelve —
Database per Service, Shared database, Event sourcing, Remote Procedure Invocation,
Domain-specific protocol, Idempotent Consumer, API Gateway, Backend for front-end, Circuit
Breaker, the two decomposition patterns, Anti-corruption layer, the two testing patterns and all
fifteen of the last instalment — carry no such line,
and are held on
[ADR-0033](../doc/handwritten/for-maintainers/adr/0033-admit-microservices-patterns-as-a-catalogue.md)'s
other ground: each is the subject matter of a chapter of the 2018 book, or predates it outright.
Earlier versions of this paragraph claimed every page carried the line. They were wrong: the
claim was made from the pages that happened to be read closely and checked properly only when
the third group was catalogued.

One trap, recorded because the next person to count will fall into it. Searching the pages for
*"my book"* returns twelve, not ten: the API Gateway page carries a MEAP announcement for the
second edition in its furniture, which is site chrome rather than a statement about the pattern.
The count above is of the body only.

**Two names were already in the catalog, and both are held twice on purpose.** This is
[ADR-0028](../doc/handwritten/for-maintainers/adr/0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.md)
applied entry by entry, and ADR-0033 states the posture for the close calls: where the work
presents the pattern and a reader could still argue it leans on an earlier source, the entry
is held. A developer who reaches for `[DomainEvent]` in a microservices codebase and does not
find it in the microservices package has been failed by the catalogue.

| Here | Already held as | Why this work presents it |
|---|---|---|
| `MicroservicesPatterns/DomainEvent` | `DomainDrivenDesign/DomainEvent` | credited to DDD in its first line, then answering a problem Evans never posed — *how does a service publish an event when it updates its data?* An aggregate emitting an event is Evans'; somebody in another process listening is not |
| `MicroservicesPatterns/SharedDatabase` | `EnterpriseIntegration/SharedDatabase` | Hohpe and Woolf present it as an integration style to choose; Richardson presents it as the thing *Database per Service* exists to escape, and names it an anti-pattern from that page. Same schema, opposite recommendation |
| `MicroservicesPatterns/RemoteProcedureInvocation` | `EnterpriseIntegration/RemoteProcedureInvocation` | a full write-up crediting nobody, answering *how do services in a microservice architecture communicate?* — which is not the question Hohpe and Woolf's integration style answers. It also says something theirs does not: the caller is unavailable for as long as the callee is, and it has to find the callee first |
| `MicroservicesPatterns/Messaging` | `EnterpriseIntegration/Messaging` | same shape of answer. Richardson's *See also* points at *Enterprise Integration Patterns* as "a comprehensive set of message patterns", which is the scholarship ADR-0028 allows rather than the passing mention it excludes — his own page carries context, problem, solution, five interaction styles and a resulting context |

One homonym is still ahead — Anti-corruption layer, in *Refactoring to services* — and it is
decided when that group is reached, not now.

`IdempotentConsumer` is a **near**-homonym of `EnterpriseIntegration/IdempotentReceiver`, and
needs no arbitration at all: the two works spell it differently, and each entry carries the
spelling its work gave it.

**`SharedDatabase` is catalogued as an anti-pattern**, which
[ADR-0023](../doc/handwritten/for-maintainers/adr/0023-admit-an-anti-pattern-on-the-same-terms-as-any-pattern.md)
already allows. It is worth more here than the clean half of the pair: *Database per Service*
is what a team says in a design review, and *shared database* is what the code actually does
for another two years. The annotation is what makes the second countable.

**`Cqrs`, not `CQRS`.** The .NET convention capitalises only the first letter of an acronym of
three letters or more, and the generated attribute follows it. The full name is in the entry's
summary, and a case-insensitive search for the word finds it.

Three shapes in this group are worth explaining, because each could have been done otherwise.

* **`DomainEvent` is flat**, one role on the event class, exactly like the DDD entry. The
  publication half of Richardson's version — the outbox, the polling publisher, the log tailing
  — is the *Transactional messaging* group, three patterns of its own. Giving this entry a
  `Publisher` role would have swallowed them.
* **`Saga.CompensatingTransaction` links the saga, not the step it undoes.** Linking the step
  is what a reader wants, and a link is a `Type`
  ([ADR-0008](../doc/handwritten/for-maintainers/adr/0008-bind-participants-with-typed-links.md))
  while a local transaction is a method — so it cannot be written. What the annotations do give
  is the count: a participant with two local transactions and one compensating transaction is
  visibly a participant the saga cannot fully back out of.
* **`ApiComposition.Composer` targets `Method` as well as a type.** A composition is often one
  controller action doing an in-memory join, and the declaration that introduces the role is
  then the method
  ([ADR-0010](../doc/handwritten/for-maintainers/adr/0010-annotate-the-declaration-that-introduces-a-role.md)).
  The same is true of `Cqrs.ViewUpdater`, which is as often a handler method as a class.

**Communication styles is the third group**, four patterns, catalogued whole, and it is the one
that meets *Enterprise Integration Patterns* head-on. Three of the four are answers to a single
question — *how do services communicate?* — and they are siblings rather than narrowings, so
nothing is related to anything: `RemoteProcedureInvocation` asks and waits, `Messaging` sends
and stops caring, `DomainSpecificProtocol` speaks SMTP or RTMP because the domain does.

`RemoteProcedureInvocation` is the only entry in this catalogue with a `Client` role, and it is
the point of the entry. The service's annotation says what it exposes; the client's says what it
has taken on — it cannot answer while the service cannot, for the length of every call, and it
must find the service before it can call it. That is where a circuit breaker and a discovery
mechanism attach, and no signature in a C# codebase shows any of it.

`DomainSpecificProtocol` is the thinnest page in the group — no forces, no resulting context —
and it is catalogued for what it **rules out** rather than for what it says. A participant that
speaks IMAP is governed by none of this catalogue's other communication machinery: no registry,
no broker, no channel. A reader who assumes the house conventions apply there is wrong in a way
that shows up in production.

`IdempotentConsumer` carries the obligation the previous group created. A message relay may
publish twice, so at-least-once delivery makes idempotence compulsory rather than desirable —
and the mechanism is a primary key on `(subscriber, message)` that lives in a schema and in no
signature. Drop the constraint and every handler still compiles and still passes its tests, on
messages that never arrive twice.

**External API and Reliability are the fourth and fifth groups**, three entries between them,
and they are the ones a reader is most likely to have come looking for: *API gateway* and
*circuit breaker* are said in standups by people who have read neither the book nor the site.

**`BackendForFrontend` is the first `specialisationOf` this catalogue records**, and it is
recorded at the pattern rather than at a role, which is the ordinary shape rather than the one
[ADR-0034](../doc/handwritten/for-maintainers/adr/0034-let-a-specialisation-name-the-role-it-narrows.md)
added. The work states it outright — *"A variation of this pattern is the Backends for frontends
pattern. It defines a separate API gateway for each kind of client"* — so every backend for
frontend **is** an API gateway, and a rule written for the broader one reaches all of them.
`ApiGateway` is flat, so the relation is attribute to attribute and loses nothing.

The work spells it two ways: *Backend for front-end* in the index, *Backends for frontends* in
the heading of the page it shares with API Gateway. The entry takes the index's spelling in the
singular, because an annotation names one participant, and this sentence is where a reader who
searched for the other spelling finds out why.

**`CircuitBreaker` is not related to anything, and the temptation was real.** The page says a
service client invokes the remote service *via a proxy*, and a circuit breaker is plainly a way
of being an RPI client — the mechanism to say so now exists. But the work does not say it, and
[ADR-0030](../doc/handwritten/for-maintainers/adr/0030-relate-only-the-narrowings-a-work-states-outright.md)
carries the narrowings a work states outright rather than the ones its arrangement suggests. The
second instalment running where having the mechanism was not a reason to use it.

What `CircuitBreaker` asserts is worth spelling out, because it is the one people annotate
carelessly: this participant **returns errors the remote service never sent**. A caller written
as though every failure came from the far end is wrong in a way that only appears when the
breaker is open, which is the worst moment to find out.

**`ApiGateway` is the entry whose annotation ages into a warning.** Hiding the partitioning is
what makes the partitioning free to change; it also gives this one participant a reason to know
about every service there is. A codebase that can list its gateways can see the day one of them
has grown back into the thing it replaced.

**Service boundaries is the sixth group, and the first this catalogue has not finished.** Two of
its four are held; two wait on the maintainer, and the reason is a rule ADR-0033 states rather
than a judgement about the patterns.

`DecomposeByBusinessCapability` and `DecomposeBySubdomain` answer one question — *how to
decompose an application into services?* — so they are siblings and nothing relates them. Their
pages share a context, a set of forces and an example list word for word, which makes it worth
saying what separates the two entries: a capability is **what the business does**, a subdomain is
**what the business means**. They usually land on the same line. Where they do not, it is because
two parts of one capability use the same noun for different things, and that is a reason to split
which no organisation chart shows.

Neither is related to `DomainDrivenDesign/CoreDomain` or `GenericSubdomain`, and could not be:
a relation never crosses a catalogue
([ADR-0027](../doc/handwritten/for-maintainers/adr/0027-ship-one-independent-package-per-catalogued-work.md)).
The classification the subdomain entry mentions — core, supporting, generic — is Evans', borrowed
by this work and spelled in its own summary rather than asserted by inheritance.

### One pattern held back, and the bar it fails

`ConsumerSideContractTest` is annotatable, carries a clear assertion — a suite verifying that a
*client* can still talk to the service it calls — is not marked `new`, and describes something that
predates the 2018 book. It is held back on
[ADR-0035](../doc/handwritten/for-maintainers/adr/0035-index-the-pattern-language-and-require-a-write-up.md)'s
second rule: **an index gloss is not a presentation.** One line of description on a bullet that links
to the page for a different pattern is not a write-up, and an entry built from it would have its
summary, its roles and every assertion written here rather than by the author.

`AntiCorruptionLayer` sets the floor — a problem and a solution, and nothing else — and this does not
reach it. If the author writes the page, the entry follows.

**`SelfContainedService` and `ServicePerTeam` were held back beside it and are now held.** Their
block was the rule ADR-0033 stated about the 2018 book, which ADR-0035 replaced: both have full
write-ups, and the `new` marker the author puts on them says his pattern language has grown, not that
the patterns are doubtful. They are the two entries this catalogue holds that the 2018 book does not
carry, which rule 3 of ADR-0035 requires be named here — and this is where they are named.

**Refactoring to services is the seventh group**, two patterns, catalogued whole — and it is the
group about leaving, which makes both entries assertions with an expiry date.

`StranglerApplication` has four roles, and the one that earns the entry is `ExtractedService`. It
carries an obligation the new code cannot show: there is, or was, code in the monolith doing this
too, and until somebody deletes it the system has two answers to one question. `NewService` is its
opposite and the work singles it out for a reason — it shows a return before any extraction is
finished, and it leaves nothing behind to remove. `Monolith` is worth annotating because a legacy
application being strangled reads exactly like one nobody intends to replace.

Two of the four role names are this catalogue's rather than the author's, and are flagged here as
`ViewUpdater` was. The page says *"there are services that implement functionality that previously
resided in the monolith"* and *"services that implement new features"* — the distinction is the
work's, the nouns `ExtractedService` and `NewService` are not.

**`AntiCorruptionLayer` is the fifth and last exact homonym**, and the only one the two works spell
differently. Evans writes *Anticorruption Layer*, Richardson writes *Anti-corruption layer*, so the
entries are `DomainDrivenDesign/AnticorruptionLayer` and `MicroservicesPatterns/AntiCorruptionLayer`
— which is
[ADR-0028](../doc/handwritten/for-maintainers/adr/0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.md)
working as intended rather than an inconsistency: a reader of either book finds the name spelled as
that book spelled it.

The two carry different assertions, which is
[ADR-0007](../doc/handwritten/for-maintainers/adr/0007-decide-sameness-by-the-assertions-a-pattern-carries.md)'s
test and the reason holding both costs nothing. Evans' has three roles — facade, adapter,
translator — and is about two bounded contexts, either of which may outlive the other. Richardson's
is flat, one role, and is about a legacy monolith: the layer exists to be deleted when the monolith
goes, so counting the layers is counting how much of the migration is still owed.

Its page is the thinnest in the catalogue — a problem and a solution, nothing else — and the entry
is still held. ADR-0033's inclusive posture covers the presentation question, and its reference
rule is satisfied by the second limb rather than the first: no book line, but the pattern predates
the 2018 book outright, being Evans' from 2003.

**Testing is the eighth group, and its index and its pages disagree about how many patterns it
has.** The index lists three bullets; there are two pages, and the third bullet points at a page
describing something else:

| Index bullet | Page it links to | Page's own title |
|---|---|---|
| Consumer-driven contract test | `testing/service-integration-contract-test.html` | **Service Integration Contract Test** |
| Consumer-side contract test | *the same page* | — the page describes the consumer-**driven** test, not this one |
| Service component sest *(sic)* | `testing/service-component-test.html` | **Service Component Test** |

The two entries take their names from the page headings, which are the author's own titles for the
patterns; *consumer-driven contract test* is the phrase most readers will search for and is written
into `ServiceIntegrationContractTest`'s summary for that reason. `ConsumerSideContractTest` is
**held back**, below, and not because it is unannotatable.

**The two are each other's mitigation**, which is the reason to hold both rather than one.
`ServiceComponentTest` is fast, cheap and reliable because it replaces everything the service
invokes — and the work states its own open issue: *how to ensure that the test doubles always
correctly emulate the behavior of the invoked services?* `ServiceIntegrationContractTest` is the
answer, and it carries an open issue of its own pointing the other way: *how to ensure that the
consumer provided tests match what the consumer actually requires?* Neither closes the loop; each
role's summary says which end it leaves open.

**`ServiceIntegrationContractTest` is annotated for one fact and one only**: the suite runs in the
provider's build and belongs to the consumer's team. Nothing in a test class shows that, and it is
what makes such a suite baffling to the people it fails.

**No `TestDouble` role here, on purpose.** `ServiceComponentTest`'s doubles are exactly what
`XUnitTestPatterns` names in five entries and separates by what each never does. A sixth, vaguer
role in this package would say less about the same class, and a relation to the real one cannot
exist across catalogues
([ADR-0027](../doc/handwritten/for-maintainers/adr/0027-ship-one-independent-package-per-catalogued-work.md)).
What this catalogue adds is `ServiceUnderTest` — the boundary of what a green run actually
covered — and the sample annotates the boundary and leaves the stub bare.

**The last six groups, and this catalogue's first exclusions.** *Service discovery*,
*Cross-cutting concerns*, *Observability*, *Security*, *UI design*, *Deployment* and the
*Architectural style* group nobody had counted: twenty-six pages, fifteen held and eleven left out.
The exclusions are in the tables at the top of this file, and three of them are worth their reasons
being read rather than skimmed.

**The six deployment patterns are excluded together, and for one reason.** They answer *how are
services packaged and deployed?* with a host, a VM image, a container image, a serverless platform
or a deployment platform. One assembly can be deployed all six ways over its life without a line
changing, so an annotation on it would distinguish nothing — which is ADR-0011's first ground stated
about time rather than about scope.

**3rd party registration is excluded by what the pattern is for.** Its stated benefit is that *the
service code is less complex than with self registration, since it is not responsible for
registering itself*. The registrar is Registrator, or Prana, or Kubernetes. The pattern is the
absence of code, and an absence has no declaration to sit on — while `SelfRegistration`, its
alternative, is annotated on the participant that does the work.

**Log aggregation and Log deployments and changes fail on different grounds**, which is why they are
in different tables. Aggregation's participant is a centralized logging service; what is in the
codebase is a logging call, which every codebase has whether or not anything aggregates it. Logging
deployments is a practice of whoever operates the application — the ground that already excludes
Continuous Integration and Evolving Order.

**`Monolithic architecture` and `Microservice architecture` close a hole rather than fill one.**
Neither was catalogued and neither was excluded for eight instalments, because the group they are in
was miscounted out of existence. What they qualify is the application, which is above the assembly
and so holds no attribute — and they are what a reader concludes *from* the annotations rather than
something an annotation adds. That is Context Map's ground, and it explains why they were never
missed: every other entry in this catalogue presupposes one of them.

Of the fifteen held, four are worth a note.

* **`HealthCheckApi` is the sharpest entry in the group.** Its verdict takes an instance out of
  rotation, so what the handler does not check is what will keep receiving traffic while broken —
  and a handler that returns healthy unconditionally is indistinguishable from one that works.
* **`DistributedTracing` fails silently or not at all.** A participant that forgets to propagate the
  identifier does not break; it ends the trace, and the gap reads as a service that was never
  called. Being able to list which participants propagate is the whole value.
* **`MicroserviceChassis` carries a prohibition rather than a capability**: no business logic, ever,
  because anything in the chassis is in every service.
* **`ServiceRegistry` is the participant whose availability bounds the application's**, and it is
  briefly wrong every time an instance dies without deregistering — which is what `HealthCheckApi`
  exists to notice.

**Two pairs of alternatives, and nothing related.** Client-side and server-side discovery answer one
question two ways; server-side and client-side UI composition likewise. Siblings, not narrowings —
the fifth instalment running where
[ADR-0030](../doc/handwritten/for-maintainers/adr/0030-relate-only-the-narrowings-a-work-states-outright.md)
records nothing.

**Transactional messaging is the second group**, three patterns, catalogued whole. It answers
the question the first group keeps running into: a service has to change its data *and* send a
message, and it cannot do both in one transaction. `TransactionalOutbox` makes it one anyway by
writing the message into a table of the same database, and the other two are the two ways of
draining that table — `PollingPublisher` asks it on a timer, `TransactionLogTailing` follows
the log the database already writes.

The four roles of the outbox are the author's own words — *Sender*, *Database*, *Message
outbox*, *Message relay* — and the one worth annotating most is `Database`. That the business
entities and the outbox live in **one** database is the entire mechanism; splitting them
compiles, and silently restores the distributed transaction the pattern exists to avoid.

**This group is where the relation ADR-0030 deferred stopped being hypothetical**, and it is
the reason the relation mechanism grew a third shape.

`PollingPublisher` and `TransactionLogTailing` are not narrowings of `TransactionalOutbox`.
They are two ways of being **one of its roles** — the work says so outright: *"There are two
patterns for implementing the Message relay."* Nothing in the schema could carry that.
`specialisationOf` related a pattern to a pattern; where the target has several roles the
generated attribute derived from its `Role` base, which would have said *a polling publisher is
a narrower case of transactional outbox* — and it is not, it is a narrower case of one of its
four participants. Recording it that way would have overstated the work, which is what
[ADR-0030](../doc/handwritten/for-maintainers/adr/0030-relate-only-the-narrowings-a-work-states-outright.md)
exists to prevent.

That is a different failure from the nine coarse relations already shipping. Where a work says
*pattern A is a kind of pattern B*, deriving from `B.Role` is true and merely coarse — a command
message really is a message. Where it says *pattern A is a way of being role R of pattern B*,
there is no true pattern-level statement at all, so the relation was not imprecise, it was
unwritable.

[ADR-0034](../doc/handwritten/for-maintainers/adr/0034-let-a-specialisation-name-the-role-it-narrows.md)
settles it: `specialisationOf` may name a **role** of the target, and the narrowing derives from
that role's attribute, which is emitted unsealed.

```csharp
public sealed class PollingPublisherAttribute : TransactionalOutbox.MessageRelayAttribute { }
```

So a rule asking *is anything draining this outbox?* gets an answer from the type system rather
than from this paragraph. Two consequences are worth knowing before writing another one. The
nine coarse relations are **not** retro-fitted — ADR-0030 still decides what may be recorded, and
a role is named only where the work names one. And a narrowing now inherits its parent role's
link properties, so `[PollingPublisher(MessageOutbox = typeof(…))]` is accepted although nothing
in that entry declares it: the surface grew somewhere the catalog does not show it.

## POSA2, and the guard that saves Scoped Locking from ADR-0011

The ninth catalogue, admitted by
[ADR-0036](../doc/handwritten/for-maintainers/adr/0036-admit-posa2-as-a-catalogue.md). Its first
instalment is **chapter 4, Synchronization: four patterns, four held.** Nothing is excluded, which
has not happened since Gang of Four, and nothing narrows anything, which is the sixth instalment
running where [ADR-0030](../doc/handwritten/for-maintainers/adr/0030-relate-only-the-narrowings-a-work-states-outright.md)
records nothing.

**Scoped Locking is admitted, on the guard rather than on the discipline.** ADR-0036 left this open
against [ADR-0011](../doc/handwritten/for-maintainers/adr/0011-leave-out-what-cannot-be-annotated.md),
and it is worth stating why it lands the opposite way from `GuardClause` at the foot of this file,
because the two look alike and are not.

What the pattern *describes* is the shape of a method body — acquire on entry, release on every
exit — and that shape holds no role, exactly as a guard clause holds none. But the pattern's
**solution names a class**: *"Define a guard class whose constructor automatically acquires a lock
… and whose destructor automatically releases the lock"*. That class is a declaration, it is the
thing a reader needs to find, and the assertion attached to it is checkable — every exit from the
scope releases. `GuardClause` has no such class to point at; it is a way of writing an `if`. The
line ADR-0011 draws is *is there a participant?*, not *is the pattern small?*

The second role is the lock the guard manages, on a field or a property, and it carries the sharper
claim of the two: that this lock is taken through the guard and never directly. A bare acquire
elsewhere in the type is then a breach of something stated rather than a difference of style.

**One participant is left out, and its own author says why.** *Double-Checked Locking
Optimization* names four participants — Just Once Critical Section, Mutex, Flag, and **Application
Thread**, of which the paper says *"It is implicit in the pseudocode"*. A participant the author
calls implicit has no declaration to sit on, so the entry holds three roles rather than four. This
is ADR-0011 applied to a role instead of to a pattern, which is the first time that has been
needed.

**Where the role names come from, stated because it is not the book.** The `reference` on all four
entries is the 2000 volume, and it is the volume that fixes these four as a chapter. The
participants, though, were read from the papers the same author published before it and still
hosts: *Strategized Locking, Thread-safe Interface, and Scoped Locking* in the *C++ Report*, and
*Double-Checked Locking* in *Pattern Languages of Program Design 3*. Those give the intents quoted
above, the two design conventions of Thread-Safe Interface — *interface methods check,
implementation methods trust* — and the Structure and Participants table the Flag and the Mutex are
taken from. Where the printed chapter names a participant differently, the entry is wrong and the
chapter wins.

**Strategized Scoped Locking is not a fifth entry.** The paper lists it as a variant of Scoped
Locking, and what it describes is the two patterns applied together: a guard parameterized by the
lock type. Two annotations already say that, so a third pattern would only say it again.

Two of the four are worth reading for the assertion rather than the name. **Thread-Safe Interface**
is the only entry in the whole catalogue whose claim is about what a method *must not call*: an
implementation method that calls back across the border self-deadlocks on a non-recursive lock, and
no compiler will mention it. **Double-Checked Locking Optimization** is the pattern famous for
being wrong — its flag has to be read and written atomically, or the thread that skips the lock can
be handed a reference published before the object behind it is built. Annotating it marks the
places to re-read, which is worth more than naming them.

### Chapter 5, Concurrency: five held, and a participant that is a state

Nine of seventeen. **Five patterns, five held, nothing excluded** — so both chapters read whole, and
what remains of POSA2 is chapters 2 and 3. No narrowing again, the seventh instalment running: the
papers relate these five to each other on every page — an active object has its own thread where a
monitor object does not, Leader/Followers is offered against Half-Sync/Half-Async — and none of it is
a work saying *this pattern is a kind of that one*, which is all ADR-0030 admits.

**Leaving a participant out has become the rule rather than a first.** Chapter 4 left out one, and
said so as a novelty. Chapter 5 leaves out five, and they are worth listing because a reader counting
the authors' participants against the roles will otherwise think entries are missing:

| Pattern | Participant | Why no role holds it |
|---|---|---|
| `LeaderFollowers` | leader, follower, processing thread | The authors describe these as roles a thread **takes turns playing** — a thread is a follower, then the leader, then a processing thread, then a follower again, within one event. A state a thread passes through has no declaration, and annotating a class with it would fix at compile time the one thing the pattern makes vary at run time. |
| `HalfSyncHalfAsync` | external I/O sources | Network interfaces, disk controllers, end-user terminals. Nothing in the codebase declares them. |
| `ThreadSpecificStorage` | application threads | The same participant, and the same reason, as *Double-Checked Locking Optimization*'s in chapter 4. |

That is [ADR-0011](../doc/handwritten/for-maintainers/adr/0011-leave-out-what-cannot-be-annotated.md)
applied to roles, five times over, and the pattern in it is clear: **what these patterns leave
unannotatable is always a thread.** Every one of the five omissions is a thread or a device, and every
participant that survives is a class, a method or a field. A vocabulary of attributes can say what a
type is for; it cannot say what a thread is currently doing.

**The name that was flagged as at risk was wrong, and so was another one.** The instalment that added
these five said Active Object's buffer might be called an *Activation List* by the book rather than the
*Activation Queue* of the paper, and that the chapter would win. A source settled it: the POSA2 tutorial
Schmidt publishes alongside the book says *"an activation list maintains pending"* and *"the scheduler
enqueues the method request into the activation list"*, and never says queue. The role is now
`ActivationList`.

The same source shows `ThreadSpecificStorage` was wrong in a way nothing had flagged. Its structure
diagram labels the participants **Thread-Specific Object**, **Thread-Specific Object Proxy** and
**Thread-Specific Object Set** — spelled out, and a *set* rather than the paper's *collection*. So the
three roles are renamed, the paragraph that justified the `TS` abbreviation as the authors' own is
withdrawn, and a fourth participant the diagram carries and the paper's list does not — the **Key
Factory** — is added.

Two things follow, and the second matters more than the first. **The flag worked**: writing down which
name was uncertain is what made it findable, and it took one source to close. **The rule needs the
better source, not the reachable one**: three of nine entries in these two chapters were built on
pre-publication papers where the book had renamed something, and only one of the three had been
suspected. Later chapters are checked against the tutorial before the entry is written rather than
after.

**Two entries say something about the platform rather than about the pattern**, and both are in the
samples rather than in the summaries:

* A monitor object on .NET has **exactly one condition, and it is the lock** — `Monitor.Wait` and
  `Monitor.PulseAll` operate on the lock object itself. So the sample annotates one field with both
  `MonitorLock` and `MonitorCondition`, which is true rather than lazy. The pattern's own example needs
  two conditions, not-empty and not-full; the way to have two here is two predicates re-tested after
  every wake.
* `ThreadSpecificObjectSet` and `KeyFactory` **will usually go unused**: the runtime supplies
  thread-local storage, so a codebase applying the pattern normally keeps neither a set nor a key
  factory of its own. Both roles are kept because the book's structure diagram carries them and a
  codebase that does keep them — one that must enumerate what every thread is holding — has nothing else
  to annotate. The sample is written as that case. Striking them is the maintainer's to do.

**Links appear in this catalogue for the first time**, in three of the five entries. Active Object is
why: six unrelated types make up one occurrence, and no type hierarchy says which proxy belongs with
which servant, which is exactly the case
[ADR-0008](../doc/handwritten/for-maintainers/adr/0008-bind-participants-with-typed-links.md) exists
for. The anchor is the proxy, because that is the participant a reader recognises.

### Chapters 2 and 3, and where each role name comes from

**Seventeen of seventeen. The catalogue is complete** — four chapters, thirty-two roles added here,
nothing excluded in any of the four. POSA2 is the first work since Gang of Four whose every pattern is
held, and the reason is the one ADR-0036 gave in advance: it is a book of object patterns, so almost
nothing in it fails ADR-0011.

Chapter 5 shipped two role names that were wrong. So the useful thing to record about these eight is
not what they claim but **where each name was read**, entry by entry, because that is what the next
correction will need:

| Entry | Role names read from | What to check |
|---|---|---|
| `WrapperFacade` | the *C++ Report* paper's participants list | — |
| `ComponentConfigurator` | the PLoP paper, **renamed** | The paper is *Service Configurator* and names Service, Concrete Service, Service Repository, Service Configurator. The book renamed the pattern to Component Configurator; the entry follows that rename through to all four roles. `ComponentRepository` is the only name not seen in any source — it is the rename applied to the paper's `Service Repository`. |
| `Interceptor` | the tutorial's class diagram | The book's chapter calls the context participant *Context Object*; the diagram box says `Context`, and that is what the entry uses. |
| `ExtensionInterface` | the tutorial's class diagram | The diagram gives Factory, Component, Root and the extending interfaces. `ComponentFactory` and `RootInterface` are the diagram's labels spelled out. |
| `Reactor` | the paper's participants list, **one renamed** | The paper calls the dispatcher an *Initiation Dispatcher*; the entry calls it `Reactor`, because the book named the pattern after that participant and no practitioner says the other. Inferred, not read. |
| `Proactor` | the paper's participants list, **one renamed** | Same shape: the paper's *Completion Dispatcher* is `Proactor` here. The paper's *Proactive Initiator* is kept as read, though the book may shorten it to `Initiator`. |
| `AsynchronousCompletionToken` | the paper's CRC cards | — |
| `AcceptorConnector` | the paper's participants list | `TransportEndpoint` is a participant the paper describes in prose rather than lists. |

Three names in that table are **inferred rather than read** — `ComponentRepository`, `Reactor` and
`Proactor` — and one more, `ProactiveInitiator`, is read from the paper against a book that may have
shortened it. That is the honest state of it. The two chapter-5 corrections were both found by writing
a flag like this one down, so the flag is the mechanism rather than an apology.

**`Client` earns a role here for the second time in the catalogue.** In
`AsynchronousCompletionToken` the client is not scenery: the token is *opaque to the service and
meaningful to the client*, so the whole pattern is a statement about which participant may read a
value. Annotating only the service and the token would leave that unsaid.

**Two roles land on a member rather than a type**, and both are the interesting part of their entry.
`WrapperFacade.Functions` goes on the platform declaration itself — in .NET, on the `extern` — and
claims it is called from the facade and nowhere else, which is precisely the leak a facade exists to
prevent and which compiles perfectly. `Proactor.AsynchronousOperation` goes on the method that starts
the operation, where the claim is that nothing written after the call has anything to do with the
outcome.

## Dependency Injection, and the target the schema did not have

The tenth catalogue, proposed by
[ADR-0037](../doc/handwritten/for-maintainers/adr/0037-admit-the-dependency-injection-catalogue.md). Its
first instalment is **chapter 4, the DI patterns: four entries, four held**, and all four are flat —
because each of these patterns *is* the declaration it names. There is nothing to choose between
participants when the participant is the constructor.

**The schema gained a target, and this is the first entry in 336 that needed one.** `AttributeTargets`
has a `Constructor` member; the enum in `pattern.schema.json` had seven of the language's kinds and not
that one, because no role until now was introduced by a constructor. `Method` does not cover
constructors — the build says so, with `CS0592` — so `ConstructorInjection` was unannotatable until the
kind was added.

That is not a new decision.
[ADR-0009](../doc/handwritten/for-maintainers/adr/0009-let-each-role-declare-what-it-applies-to.md)
already decides that a role declares what it applies to; the set of kinds available is the C# language's
and not this repository's, and the enum was a subset that had simply never been asked for the eighth
member. Nor does it leave machinery unused, which is
[ADR-0031](../doc/handwritten/for-maintainers/adr/0031-carry-no-generator-machinery-for-an-unused-capability.md)'s
concern: the entry that adds the kind uses it, and two more of this work's items will — *Constrained
Construction* and *Constructor Over-injection* are both about a constructor.

**The edition is named before an instalment can rest on the wrong one**, which is ADR-0037's follow-up
and ADR-0035's lesson applied in advance. The list comes from the **2019 second edition**, by van
Deursen and Seemann. The 2011 first edition — Seemann alone, titled *Dependency Injection in .NET* — has
a different chapter arrangement and a different set of anti-patterns, and is not what `reference` names.

**Where the four came from**, entry by entry, on the discipline the POSA2 chapters arrived at the hard
way:

| Entry | Read from |
|---|---|
| `CompositionRoot` | Seemann's own definition and his rule that a DI container is referenced from there and nowhere else — his blog, where he named the pattern in 2011 |
| `ConstructorInjection` · `MethodInjection` · `PropertyInjection` | the publisher's section-level contents, which name each pattern and its *How it works* / *When to use it* sections. The names are the mechanism, so there is no participant to get wrong; what is written from the sections rather than quoted is the **claim** each carries — required, per-invocation, optional-with-a-default |

Manning publishes a free article per pattern. They are behind a captcha, and were not read; nothing here
rests on them.

**The claims are of a kind the catalogue has not carried before.** `CompositionRoot`'s is checkable
against *assembly references* — no module but this one may reference the container — rather than against
the shape of any code. `PropertyInjection`'s is the sharpest of the four: it asserts that a working
default exists, so a property injection without one is a required dependency that has forgotten to fail,
and it fails later, on a null reference, far from the declaration that promised otherwise.

### Chapter 5, the anti-patterns, and what the annotation does not do

Eight of eleven. **Four entries, five roles**, and the chapter is complete — Control Freak, Service
Locator, Ambient Context, Constrained Construction. What is left is §8.3's three lifestyles.

**The samples are the same radio station as chapter 4, and deliberately so.** Chapter 4 showed the
shapes the station moved *to*; these four are what it has not moved yet — eleven classes that construct
their own dependencies, four resolve calls inside a plug-in host with no seam to inject through,
sixty-one call sites on a static clock, and a processor chain loaded by reflection. Nobody writes these
on purpose. They are what a codebase has before somebody asks the question.

That matters because it is the only use these four entries have. **An anti-pattern annotation is not
detection**: one that annotates itself is an honest offender, and the one worth catching is the one
nobody marked. Its use is a **baseline** — the count of what is known and accepted, held by a build at
*no more than eleven, and never more*, which is the only architecture rule that works on code that
already exists. Without the annotation the rule cannot be written at all, because nothing distinguishes
the eleven that were accepted from the twelfth added next Tuesday. It is the same instrument as
`PublicAPI.Shipped.txt` and RS0016, in the domain's words instead of the compiler's, and
[ADR-0037](../doc/handwritten/for-maintainers/adr/0037-admit-the-dependency-injection-catalogue.md)
turns on it: a shape can be counted, and a degree cannot, which is why chapter 6 is out.

**`ServiceLocator` is the only one of the four with two roles**, and the split is the point. A codebase
has one registry against many consumers. The role on the registry marks the *boundary*, so a rule can
range over everything that references it; the role on the consumer carries the *cost*, and it is
Seemann's own: the class does not state its preconditions, so a missing registration fails at run time
and adding a dependency inside it is a breaking change that breaks no build.

**And the annotation takes no side in a live disagreement.** Fowler named Service Locator as a pattern
in 2004 and leans toward it for application code — *"I don't see the injector's inversion as providing
anything compelling"* where the consumer is your own application. Seemann calls it an anti-pattern.
This catalogue holds Seemann's entry because Seemann's is the work catalogued; Fowler's is absent
because the 2004 article is not one of the works here, and a reader should know that the index shows one
side of the argument. What the attribute records either way is a structural fact — *the preconditions
are not in the contract* — and the verdict belongs to whoever writes the rule.

**`ConstrainedConstruction` is the second use of the `Constructor` target**, as ADR-0037 predicted when
the kind was added. It sits on the constructor rather than on the loader that constrains it, because the
constructor is where the constraint lands and where a reader meets the puzzle: a class with an obvious
dependency that declares none, for a reason three files away.

**One entry has changed classification between the work's own editions.** Seemann's 2010 post says *"My
book contains a section on the **Ambient Context pattern**"*; the 2019 edition files Ambient Context
under chapter 5, the anti-patterns. Same author, same shape, different verdict eight years apart. The
catalogue follows the 2019 edition, and this is the concrete instance of why ADR-0037 names an edition
rather than a work.

### The lifestyles, and four concepts this catalogue has not decided

Eleven of eleven. **Three entries, three roles**, all flat, and the catalogue is complete against what
ADR-0037 admits.

**A lifestyle annotation is a constraint on the class, not a description of the registration.** The
composition root's `AddSingleton` line says what the container was told; it says nothing about what that
obliges the class to be. `[SingletonLifestyle]` does: used concurrently, therefore thread-safe, holding
nothing belonging to one caller, and depending only on things that live at least as long. That is the
first claim in this base checkable **against configuration in both directions** — every class marked
here should be registered once, and every class registered once should be marked.

The three obligations are worth separating, because each entry carries a different one:

| Entry | What the class owes |
|---|---|
| `SingletonLifestyle` | thread-safety, no per-caller state, and no shorter-lived dependency captured |
| `TransientLifestyle` | nothing about state — but if it is disposable, a disposal nobody arranged is a leak nothing reports |
| `ScopedLifestyle` | safety only within one scope, and never reached from outside one |

**Nothing stops a class carrying two of them.** The generator emits three independent attributes and
`AllowMultiple` is false on each, so the compiler refuses a repeat of the *same* lifestyle and permits a
`[SingletonLifestyle]` beside a `[TransientLifestyle]`. That is a rule for a reader to write — *no
declaration carries more than one lifestyle* — and it is named here because nothing in the vocabulary
expresses mutual exclusion between patterns.

**Four concepts the work names are left undecided, and ADR-0037 said this instalment would face them.**
They sit outside its three catalogue sections, so the record admits nothing about them; it asks for a
decision when chapter 8 is reached, and it is reached. The recommendation below is not a decision:

| Concept | Where | Recommendation |
|---|---|---|
| `CaptiveDependency` | §8.4.1 | **Exclude, on Context Map's ground.** It is what a reader *concludes from* the annotations rather than a participant: a `[SingletonLifestyle]` class holding a `[ScopedLifestyle]` one **is** a captive dependency, so a rule derives it from what is already annotated and an entry would annotate a conclusion |
| `LeakyAbstraction` | §8.4.2 | **Exclude**, for consistency with ADR-0037's refusal of the smells — *leaky* is a judgement rather than a shape |
| `StableDependency`, `VolatileDependency` | §1.3 | **Admit**, if the maintainer will have them. The classification is binary, the authors give criteria for it, it sits on an abstraction, and *is this dependency volatile?* is the question that decides whether to inject at all — but they are outside the catalogue sections, so ADR-0037 does not cover them and a record would have to |

## Shape of the generated attribute

A pattern whose single role carries the pattern's own name is emitted flat, so
that it reads as ubiquitous language:

```csharp
[ValueObject] public readonly record struct Money(decimal Amount, string Currency);
```

Every other pattern is emitted as a static container holding one sealed
attribute per role, so that an annotation still reads as *this is a X* rather
than *this belongs to pattern X*:

```csharp
[Composite.Component]                       public interface INode { }
[Composite.Leaf(Component = typeof(INode))] public sealed class FileNode : INode { }
```

A role targeting `Method` is a member role. Nothing else distinguishes it: it is
generated exactly like the others, and consumers tell them apart by reading
`AttributeUsage`.

## Held back for want of a source

`Idioms` is for a pattern that has a **source** but no body of work of its own
(ADR-0013) — it names the absence of a catalog, not the absence of a source, and
every entry must record a reference with a year, because that reference is what says
which work presents the pattern as its own (ADR-0028).

Two everyday practices fail that, and one of them is named in ADR-0013 itself as
the example of an Idioms candidate:

| Held back | What was looked for, and found |
|---|---|
| `Result` | No publication names it as a pattern. Its lineage runs through Haskell's `Either` — a general sum type, not error handling — and Rust's `Result`, a standard-library type rather than a named pattern. Recording either as *the work that named it* would be false. |
| `Option` / `Maybe` | Same shape of problem, with a better-looking answer that does not survive inspection: `option` is defined in *The Definition of Standard ML* and `Maybe` in the Haskell report, but those works define a **type**, not a pattern, and neither is a body of work about patterns. |

Both would be useful entries. Admitting them means one of two things, and neither
is a detail: find a publication that genuinely named the practice, or decide that
`Idioms` may hold a pattern whose provenance is a lineage rather than a work —
which is a change to ADR-0013 and to the schema's required reference, and belongs
in a record of its own rather than in a catalog entry written quietly.

`GuardClause` was looked at with them and is closed rather than held back: it is a
shape a method body takes, so nothing holds a role and nothing can be asserted
about a participant (ADR-0011). POSA2's Scoped Locking reads as the same case and
is not — its solution names a guard class, which is a participant — and the
difference is set out above.
