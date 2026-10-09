# Contributing

Read [`AGENTS.md`](AGENTS.md) first: it carries the ADR check, the sequence for
adding a pattern, and the conventions the compiler will not enforce. This guide
covers the rest — how the repository is built, and how commits are written.

## Building

```
dotnet build DesignPatternCatalog.sln
dotnet test DesignPatternCatalog.sln
dotnet run --project DesignPatternCatalog.Usage
```

The library multi-targets `netstandard2.0` through `net8.0`; a change that
compiles on the newest target may not compile on the oldest, so build the
solution rather than one framework. The sample project prints the whole catalog
read back through the base attribute alone — that inventory is the check that a
catalog change landed.

The attributes carry no behaviour, so nothing tests what code does. The suite
asserts what every generated attribute must *look* like — it derives from the
base, it declares what it applies to, every role of one pattern answers one
identity, a link names a role of the same pattern — and what the reading rules
answer for each shape the generator emits. A defect written into the template is
emitted uniformly across the catalog and survives the round trip; these are what
catch it.

Alongside them, CI proves that every role compiles onto a plausible participant,
that the catalog is valid, that the whole of it reads back, and that regenerating
an unchanged catalog leaves the working tree clean.

## Changing the catalog

Never hand-edit a generated attribute, nor the catalog index. Edit
`catalog/<Catalog>/<Pattern>.json`, then:

```
python3 catalog/generate.py
python3 tools/catalog/validate.py     # needs: pip install -r tools/catalog/requirements.txt
```

## The public API baseline

These libraries ship public types and nothing else, so their public surface is the
whole of the product. It is declared in `<project>/PublicAPI/` — **one baseline per
package** since ADR-0027 split the catalogues, each shared by all six target
frameworks. The attributes are the same on every framework, so a shared file makes a
divergence between two targets a failure rather than something two baselines would
absorb; and a baseline per package means a change to one work's surface cannot hide
in another's diff.

An undeclared public symbol raises `RS0016`; a declared symbol that no longer
exists raises `RS0017`. Both are warnings locally and errors in CI, so a surface
change cannot merge until the same change updates the baseline.

**Accepting an intended surface change.** Update the baseline in the same commit:

```
dotnet format analyzers DesignPatternCatalog.<Catalog>/DesignPatternCatalog.<Catalog>.csproj \
  --diagnostics RS0016 --severity warn
```

That appends the new entries to `PublicAPI.Unshipped.txt`. A **removal** is
deleted by hand — deliberately, since a removal is a breaking change and deleting
the line is the moment to notice it.

The generator does not write the baseline, and must not: a baseline written by
the thing it checks would always agree with itself, and would rewrite itself to
match exactly the template change it exists to catch (ADR-0018).

Everything sits in `PublicAPI.Unshipped.txt` today because nothing has been
published. After **every** release, the entries of each package it published are promoted
from `PublicAPI.Unshipped.txt` to `PublicAPI.Shipped.txt`, by hand, in a commit of their
own: the shipped file is what says what consumers received, and an entry left in the
unshipped one can be deleted without the analyzer noticing a removal.

## Versioning

The packages follow Semantic Versioning over **two** contracts, not one: what a
consumer compiles against, and what it reads back. The attributes carry no
behaviour and the libraries ship no reader, so a change can leave the public
surface byte-identical and still change every consumer's answers.

**One version per package.** Each package is released from its own tag and moves on its own
(ADR-0044); the first version of every package is `1.0.0` (ADR-0045).

| | |
|---|---|
| **Major** | a role or pattern removed or renamed · a target set narrowed · `AllowMultiple` or `Inherited` changed · a pattern moved between catalogs, which now moves it between packages · a relation added or removed · a reading rule changed |
| **Minor** | a pattern added · a role added to a published pattern · a target set widened · a link added to a role |
| **Patch** | documentation, samples, the catalog index, anything that reaches no consumer |

The two rows worth reading twice are in the major line. **A relation** — declaring
that one pattern narrows another — reads as an editorial remark and is in fact a
change to what `IdentityOf` answers for annotations already written. **A reading
rule** reads as documentation and is what consumers copy.

## Releasing

A release is a tag, and the tag is the only input. Tag a commit of `main` once its CI is green:

| Tag | Publishes |
|---|---|
| `core-vX.Y.Z` | `Core` at `X.Y.Z`, then **every** catalogue and the meta-package, each from its own last version: the next major when `Core` took a major step, the next patch otherwise |
| `<catalogue>-vX.Y.Z` (`gangoffour`, `reefact`, …) | that catalogue, then the meta-package at the same kind of step (patch, minor or major) the tag takes over the catalogue's previous one |
| `all-vX.Y.Z` | the meta-package alone |

The first release is `core-v1.0.0`, which publishes every package at `1.0.0`; the first tag of any package is
exactly `1.0.0`. A tag must be exactly one step above the previous tag of its package — the next patch, the next minor with patch `0`, or the next
major with minor and patch `0` — and **whoever picks the number decides whether the change is breaking**,
using the table above. `tools/release/plan.py` refuses a number that rule could not have produced.

`.github/workflows/release.yml` plans the release, builds, tests, packs and publishes. A pushed tag needs
the `NUGET_API_KEY` secret and fails at once without it: a tag stays in the repository, and the planner
reads every tag as a release, so a tag that published nothing would leave a version on record that nobody
can install. To see what a tag would do, run the workflow by hand (*Run workflow*) with the tag as input:
it plans, builds, tests and packs, and publishes and tags nothing.

The packages a cascade moves are tagged afterwards, in one atomic push, so the next release starts from the
right numbers. **If a release fails part way, run the workflow again on the same tag** — a package already
pushed is skipped — rather than tagging the next number. Releases are processed one at a time, in the order
their tags arrive. Reasoning: ADR-0044, ADR-0045.

## Enabling the commit-message hook

A `commit-msg` hook checks every message against the convention below before it
is recorded. It is versioned under `.githooks/`; enable it once per clone:

```
git config core.hooksPath .githooks
```

The same script runs in CI on every pull request, so a bypassed hook
(`git commit --no-verify`) is caught before merge. Merge commits are exempt.

## Commit convention

```
<type>[(<scope>[,<scope>...])][!]: <description>

<body>

<footers>
```

The header is validated in full and must fit within **72 characters**.

### Type

One of `feat`, `fix`, `build`, `chore`, `ci`, `docs`, `perf`, `refactor`,
`revert`, `style`, `test`.

### Scope

Optional, and names a component — never a file or a class. One of:

| Scope | What it covers |
|---|---|
| `attributes` | the generated attribute sources and the base marker |
| `catalog` | the JSON catalog, its schema and the generator |
| `usage` | the sample project |
| `doc` | the ADR base and the handwritten documentation |
| `build` | the build, the workflows and the development-time tooling |

Several scopes are comma-separated, with no space, unique and alphabetical:
`feat(attributes,catalog): …`.

A scope must say what the type does not, so one that repeats the type is left out
wherever it appears — not only where it stands alone. The type already says the
change is documentation, or the build; a scope beside it names the *other*
components reached. So `docs(doc)` is `docs:`, `docs(build,doc)` is
`docs(build):`, and `build(build)` is `build:`. The repetition is rejected.

The same reasoning, one step further, leaves out `usage` beside `catalog`: ADR-0012
requires a worked sample for every pattern, so adding a pattern always touches the
sample project. `feat(catalog,usage): add Splitter` tells a reader nothing
`feat(catalog): add Splitter` does not. Write `catalog` alone; the scope stays for a
change that reaches the samples and nothing else. Nothing rejects this one — it is a
convention, and the header limit is tight enough that the six wasted characters are
worth having back.

### Description

Imperative and lowercase — *add*, not *Add* or *Added* — and no trailing period.

### Breaking changes

A breaking change is signalled **twice**: a `!` before the colon, and a
`BREAKING CHANGE:` footer describing the migration. One without the other is
rejected, because either alone is easy to miss — the `!` by a reader skimming
headers, the footer by tooling reading only the header.

```
feat(attributes)!: drop the role enumerations

BREAKING CHANGE: a consumer switching on a role enumeration now switches on
the attribute type instead.
```

### Issue footer

When a commit refers to an issue, the footer reads exactly `Refs: #<number>`.

### Autosquash placeholders

`fixup!`, `squash!` and `amend!` headers are allowed locally — the hook lets them
through so that a rebase can still absorb them — and rejected in CI, so that one
cannot land unsquashed in `main`.
