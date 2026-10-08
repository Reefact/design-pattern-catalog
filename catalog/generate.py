#!/usr/bin/env python3
"""Regenerates the attribute sources from the pattern catalog.

    python3 catalog/generate.py

Reads every catalog/<Catalog>/<Pattern>.json and rewrites the matching
DesignPatternCatalog.<Catalog>/<Pattern>.cs. The generated
sources are committed and are what ships; this script only keeps them uniform.
A pattern whose single role carries the pattern's own name is emitted as a flat
attribute, every other pattern as a static container holding one attribute per
role.
"""

import glob
import json
import os
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
INDEX_DIR = os.path.join(REPO, "doc", "generated")
NS = "DesignPatternCatalog"

CATALOG_LABEL = {
    "GangOfFour": "Gang of Four",
    "DomainDrivenDesign": "Domain-Driven Design",
    "EnterpriseApplicationArchitecture": "Patterns of Enterprise Application Architecture",
    "AnalysisPatterns": "Analysis Patterns",
    "AccountingPatterns": "Accounting Patterns",
    "EnterpriseIntegration": "Enterprise Integration Patterns",
    "XUnitTestPatterns": "xUnit Test Patterns",
    "MicroservicesPatterns": "Microservices Patterns",
    "Posa2": "Pattern-Oriented Software Architecture, Volume 2",
    "DependencyInjection": "Dependency Injection Principles, Practices, and Patterns",
    "Reefact": "Reefact",
    "Idioms": "no catalog of its own",
}


def relation(pattern):
    """The pattern this one narrows, if any.

    Only one kind of relation is left. A declension — the same pattern named by two works — needed the two
    catalogues to refer to each other, and since ADR-0027 each ships as its own package with no reference to
    another, so it can no longer exist. A specialisation stays, inside one catalogue.
    """
    return pattern.get("specialisationOf")


def key(pattern):
    return pattern["catalog"], pattern["name"]


def role_names(pattern):
    return [role["name"] for role in pattern["roles"]]


def base_of(pattern):
    """What the generated construct inherits from.

    A pattern with one role inherits attribute-to-attribute; a pattern with several inherits through the
    abstract role base its container declares, which is what every one of its roles answers. Resolved in
    main(), where the whole catalog is known, since only the target's own entry says which of the two it is.
    """
    return pattern["_base"]


def relation_doc(pattern):
    target = relation(pattern)
    if target is None:
        return None
    if target.get("role"):
        # The work said this is a way of being one participant, not a way of being the whole pattern
        # (ADR-0034), and the sentence has to say the same thing the inheritance does.
        return (f"A narrower case of {target['name']}'s {target['role']} role: every participant annotated "
                f"here is one of those too, and a consumer asking for that role gets these as well.")
    return (f"A narrower case of {target['name']}: every participant annotated here is one of those too, and a "
            f"consumer asking for the broader pattern gets these as well.")


def reference_doc(pattern):
    ref = pattern["reference"]
    return f"{ref['author']}, <i>{ref['work']}</i>, {ref['year']}."


def remarks(paragraphs, indent):
    """A single <remarks> block, one <para> per paragraph."""
    pad = " " * indent
    lines = [f"{pad}/// <remarks>"]
    for paragraph in paragraphs:
        if paragraph is None:
            continue
        lines.append(f"{pad}///     <para>")
        lines += [f"{pad}///         {line}" for line in textwrap.wrap(paragraph, width=108 - indent)]
        lines.append(f"{pad}///     </para>")
    lines.append(f"{pad}/// </remarks>")
    return "\n".join(lines)


def doc(text, indent, tag="summary"):
    """XML documentation block, wrapped the way the rest of the sources are."""
    pad = " " * indent
    lines = [f"{pad}/// <{tag}>"]
    lines += [f"{pad}///     {line}" for line in textwrap.wrap(text, width=112 - indent)]
    lines.append(f"{pad}/// </{tag}>")
    return "\n".join(lines)


def targets(names):
    return " | ".join(f"AttributeTargets.{name}" for name in names)


def header(catalog):
    return [
        "#region Usings declarations",
        "",
        "using System;",
        "",
        "#endregion",
        "",
        f"namespace {NS}.{catalog} {{",
        "",
    ]


def role_class(pattern, role, indent):
    pad = " " * indent
    # Multiplicity comes from the catalog, not from the targets. Deriving it worked only for as long as the
    # rule "a member holds its role once, anything else may repeat" happened to hold; an assembly is one
    # bounded context rather than several, and no rule over target kinds recovers that (ADR-0009).
    allow_multiple = "true" if role["repeatable"] else "false"
    inherited = "true" if pattern["inherited"] else "false"

    out = [doc(role["summary"], indent)]
    out.append(f"{pad}[AttributeUsage({targets(role['targets'])}, "
               f"AllowMultiple = {allow_multiple}, Inherited = {inherited})]")
    if not role["links"] and not role.get("externalLinks"):
        out.append(f"{pad}public {role['_modifier']}class {role['name']}Attribute : Role {{ }}")
        return "\n".join(out)

    out.append(f"{pad}public {role['_modifier']}class {role['name']}Attribute : Role {{")
    out += link_properties(role, indent + 4)
    out.append("")
    out.append(f"{pad}}}")
    return "\n".join(out)


def link_properties(role, indent):
    """The optional typed properties a role carries: links to its siblings, then links to any other type.

    A link to a sibling names a role of the same pattern and is documented as such (ADR-0008). An external link
    names a type that is no role of the pattern — the one thing the hierarchy cannot say — and carries its own
    sentence, since there is no sibling attribute for the reader to follow.
    """
    pad = " " * indent
    out = []
    for link in role["links"]:
        out.append("")
        out.append(doc(f'The <see cref="{link}Attribute" /> this role is bound to. Optional: it is only needed '
                       f"when the type hierarchy alone does not tell which occurrence of the pattern is meant.",
                       indent))
        out.append(f"{pad}public Type? {link} {{ get; init; }}")
    for link in role.get("externalLinks", []):
        out.append("")
        out.append(doc(link["summary"], indent))
        out.append(f"{pad}public Type? {link['name']} {{ get; init; }}")
    return out


def flat_attribute(pattern):
    """Single-role pattern: a flat attribute, with neither nesting nor argument."""
    name = pattern["name"]
    inherited = "true" if pattern["inherited"] else "false"

    out = header(pattern["catalog"])
    out.append(doc(f"{name} ({CATALOG_LABEL[pattern['catalog']]}) — {pattern['summary']}", 4))
    out.append(remarks(["This pattern has a single role, so there is nothing to choose: the attribute is "
                        "applied on its own.",
                        relation_doc(pattern),
                        reference_doc(pattern)], 4))
    # A specialisation is a pattern of its own, and may legitimately accept fewer targets than the pattern it
    # narrows. Multiplicity comes from the catalog: a flat pattern's declared multiplicity used to be written
    # down here and then ignored, so the catalog said one thing and the shipped attribute another.
    role = pattern["roles"][0]
    out.append(f"    [AttributeUsage({targets(role['targets'])}, "
               f"AllowMultiple = {'true' if role['repeatable'] else 'false'}, Inherited = {inherited})]")
    if role.get("externalLinks"):
        out.append(f"    public {pattern['_modifier']}class {name}Attribute : {base_of(pattern)} {{")
        out += link_properties(role, 8)
        out.append("")
        out.append("    }")
    else:
        out.append(f"    public {pattern['_modifier']}class {name}Attribute : {base_of(pattern)} {{ }}")
    out.append("")
    out.append("}")
    return "\n".join(out) + "\n"


def nested_container(pattern):
    """Multi-role pattern: a static container plus one attribute per role."""
    name = pattern["name"]

    out = header(pattern["catalog"])
    out.append(doc(f"{name} ({CATALOG_LABEL[pattern['catalog']]}) — {pattern['summary']}", 4))
    out.append(remarks(["Annotate the declaration that introduces the role. When a role is introduced by an "
                        "interface, annotate that interface rather than each of its implementations.",
                        relation_doc(pattern),
                        reference_doc(pattern)], 4))
    out.append(f"    public static class {name} {{")
    # Every pattern gathers its roles under one abstract base — the type every role of the pattern answers,
    # and what a specialisation inherits from in order to answer the broader one as well.
    out.append("")
    out.append(doc(f"Role played by a type or a member in the {name} design pattern.", 8))
    out.append(f"        public abstract class Role : {base_of(pattern)} {{ }}")
    for role in pattern["roles"]:
        out.append("")
        out.append(role_class(pattern, role, 8))
    out.append("")
    out.append("    }")
    out.append("")
    out.append("}")
    return "\n".join(out) + "\n"


def find_samples():
    """Where each pattern's sample actually lives, rather than where a rule would put it.

    Most samples sit in the one sample project, one file per pattern. A pattern whose roles are held by an
    assembly cannot: an assembly makes one set of claims, so showing several of them needs several sample
    assemblies, and no rule over the catalog derives their names. Looking the file up keeps the index
    truthful whatever the layout — and makes a pattern with no sample at all say so, in the one document a
    reader browses.
    """
    found = {}
    for path in sorted(glob.glob(os.path.join(REPO, "*Usage*", "**", "*Usage.cs"), recursive=True)):
        name = os.path.basename(path)[: -len("Usage.cs")]
        relative = os.path.relpath(path, REPO).replace(os.sep, "/")
        # Keyed by catalog AND name, because a name is not unique: ValueObject is held by two catalogs and
        # Repository by two, and keying on the file name alone linked Fowler's entries to Evans' samples.
        # The bare name stays as a fallback for a pattern whose sample lives in a sample assembly of its
        # own, where there is no catalog directory to match on.
        for key in ((relative.split("/")[1] if relative.count("/") > 1 else None, name), (None, name)):
            found.setdefault(key, relative)

    return found


SAMPLES = {}


def is_single_role(pattern):
    return len(pattern["roles"]) == 1 and pattern["roles"][0]["name"] == pattern["name"]


def annotation_of(pattern, role):
    """How the role is written at a declaration — the thing a reader of the index is looking for."""
    return f"[{role['name']}]" if is_single_role(pattern) else f"[{pattern['name']}.{role['name']}]"


def anchor_of(pattern):
    """A heading unique across catalogs: ValueObject is held by two of them."""
    label = CATALOG_LABEL[pattern["catalog"]]
    slug = f"{pattern['name']} ({label})".lower().replace(" ", "-")

    return "".join(c for c in slug if c.isalnum() or c == "-")


def relation_line(pattern):
    target = relation(pattern)
    if target is None:
        return None
    return f"A narrower case of **{target['name']}**: every participant here is one of those too."


def index_entry(pattern):
    """One pattern, as the index shows it."""
    name = pattern["name"]
    label = CATALOG_LABEL[pattern["catalog"]]

    out = [f"### {name} ({label})", "", pattern["summary"], "", f"*{reference_doc(pattern)}*".replace("<i>", "").replace("</i>", "")]

    line = relation_line(pattern)
    if line is not None:
        out += ["", line]

    out += ["", "| Role | Annotation | Applies to | Repeatable | Links |", "|---|---|---|---|---|"]
    for role in pattern["roles"]:
        targets_read = ", ".join(target.lower() for target in role["targets"])
        repeatable = "yes" if role["repeatable"] else "no"
        links = ", ".join([f"`{link}`" for link in role["links"]]
                          + [f"`{link['name']}` (any type)" for link in role.get("externalLinks", [])]) or "—"
        out.append(f"| {role['name']} | `{annotation_of(pattern, role)}` | {targets_read} | {repeatable} | {links} |")

    for role in pattern["roles"]:
        out += ["", f"**{role['name']}** — {role['summary']}"]

    source = f"../../{NS}.{pattern['catalog']}/{name}.cs"
    sample = SAMPLES.get((pattern["catalog"], name)) or SAMPLES.get((None, name))
    where = f"[Sample](../../{sample})" if sample else "**no sample**"
    out += ["",
            f"Held by a subtype: {'yes' if pattern['inherited'] else 'no'} · "
            f"[Source]({source}) · {where}"]

    return "\n".join(out)


def index_document(patterns):
    """The catalog as a reader browses it, rather than as the compiler consumes it."""
    roles = sum(len(pattern["roles"]) for pattern in patterns)
    catalogs = sorted({pattern["catalog"] for pattern in patterns})

    out = ["# The catalog",
           "",
           "<!-- Generated by catalog/generate.py from catalog/<Catalog>/<Pattern>.json. Do not edit. -->",
           "",
           f"**{len(patterns)} patterns, {roles} roles**, across {len(catalogs)} catalogs. A pattern is "
           "catalogued in the body of work that named it, under the name that work gave it — so a reader of a "
           "book finds its patterns spelled as it spelled them, and two works that name one pattern are "
           "related rather than merged.",
           "",
           "## Every pattern",
           "",
           "| Pattern | Catalog | Roles | Related to |",
           "|---|---|---|---|"]

    for pattern in sorted(patterns, key=lambda p: (p["name"], p["catalog"])):
        target = relation(pattern)
        related = "—" if target is None else f"narrows {target['name']}"
        out.append(f"| [{pattern['name']}](#{anchor_of(pattern)}) | {CATALOG_LABEL[pattern['catalog']]} | "
                   f"{len(pattern['roles'])} | {related} |")

    for catalog in catalogs:
        owned = sorted((p for p in patterns if p["catalog"] == catalog), key=lambda p: p["name"])
        out += ["", f"## {CATALOG_LABEL[catalog]}", "",
                f"`{NS}.{catalog}` — {len(owned)} patterns, "
                f"{sum(len(p['roles']) for p in owned)} roles.", ""]
        out += ["\n".join([index_entry(pattern), ""]) for pattern in owned]

    return "\n".join(out).rstrip() + "\n"


def main():
    patterns = []
    for path in sorted(glob.glob(os.path.join(HERE, "*", "*.json"))):
        with open(path, encoding="utf-8") as handle:
            patterns.append(json.load(handle))

    index = {key(pattern): pattern for pattern in patterns}

    # Nothing is unsealed that is not actually derived from, so the exceptions in the generated sources are
    # explained by the catalog rather than by the template. A specialisation narrows a whole pattern or one
    # of its roles (ADR-0034), so both a pattern and a role can be the thing something derives from, and
    # each is unsealed exactly when some entry names it.
    unsealed_patterns = set()
    unsealed_roles = set()
    for pattern in patterns:
        target = relation(pattern)
        if target is None:
            continue
        if target["catalog"] != pattern["catalog"]:
            raise SystemExit(f"{pattern['name']}: narrows {target['catalog']}.{target['name']}, which is in "
                             f"another catalogue. Each catalogue ships as its own package with no reference to "
                             f"another, so the inheritance this would emit cannot exist (ADR-0027)")
        base = index.get((target["catalog"], target["name"]))
        if base is None:
            raise SystemExit(f"{pattern['name']}: derives from {target['catalog']}.{target['name']}, "
                             f"which is not in the catalog")
        if target.get("role"):
            if is_single_role(base):
                raise SystemExit(f"{pattern['name']}: names the role {target['role']} of "
                                 f"{target['name']}, which is flat — a flat target is already derived from "
                                 f"attribute to attribute, so naming its role adds nothing")
            if target["role"] not in role_names(base):
                raise SystemExit(f"{pattern['name']}: narrows the role {target['role']}, which is not a role "
                                 f"of {target['name']}")
            unsealed_roles.add((*key(base), target["role"]))
        elif is_single_role(base):
            unsealed_patterns.add(key(base))

    for pattern in patterns:
        target = relation(pattern)
        if target is None:
            pattern["_base"] = "DesignPatternAttribute"
        elif target.get("role"):
            # Same catalogue, so the same namespace: no prefix needed, and none possible for another.
            pattern["_base"] = f"{target['name']}.{target['role']}Attribute"
        else:
            base = index[(target["catalog"], target["name"])]
            pattern["_base"] = (f"{base['name']}Attribute" if is_single_role(base)
                                else f"{base['name']}.Role")
        pattern["_modifier"] = "" if key(pattern) in unsealed_patterns else "sealed "
        for role in pattern["roles"]:
            role["_modifier"] = "" if (*key(pattern), role["name"]) in unsealed_roles else "sealed "

    for pattern in patterns:
        # One project per catalogued work, since ADR-0027 ships each as its own package.
        folder = os.path.join(REPO, f"{NS}.{pattern['catalog']}")
        os.makedirs(folder, exist_ok=True)
        body = flat_attribute(pattern) if is_single_role(pattern) else nested_container(pattern)
        with open(os.path.join(folder, pattern["name"] + ".cs"), "w", encoding="utf-8") as handle:
            handle.write(body)

    # Several hundred patterns are not navigable through a directory listing, and the generated sources are
    # the wrong place to browse: they are read by a compiler, one file at a time. The index is the catalog
    # as a reader meets it — what exists, under which name, with which roles, and where to see it at work.
    SAMPLES.update(find_samples())
    os.makedirs(INDEX_DIR, exist_ok=True)
    with open(os.path.join(INDEX_DIR, "catalog-index.md"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(index_document(patterns))

    for catalog in sorted({pattern["catalog"] for pattern in patterns}):
        owned = [p for p in patterns if p["catalog"] == catalog]
        print(f"{catalog}: {len(owned)} patterns, {sum(len(p['roles']) for p in owned)} roles")
    print(f"TOTAL: {len(patterns)} patterns, {sum(len(p['roles']) for p in patterns)} roles")


if __name__ == "__main__":
    main()
