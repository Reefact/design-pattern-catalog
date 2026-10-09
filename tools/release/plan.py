#!/usr/bin/env python3
"""Plans a release from the tag that triggered it.

    python3 tools/release/plan.py --tag core-v1.0.0 --props build/Versions.generated.props --plan plan.json

Every package is released from a tag named `<package>-v<MAJOR>.<MINOR>.<PATCH>`: `core`, `all` (the
meta-package), or the lower-cased catalogue name (`gangoffour`, `reefact`, ...). The tag is the only input:
which packages are published, and at which version, follows from it and from the tags that already exist.

* `core-vX.Y.Z` publishes Core at X.Y.Z, then every catalogue and the meta-package from THEIR OWN last version:
  a major step of Core is breaking and moves each of them to the next major, anything else moves each to the
  next patch. A package that has never been released starts at 1.0.0.
* `<catalogue>-vX.Y.Z` publishes that catalogue, then the meta-package at the same level of step (patch,
  minor or major) that the tag takes over the catalogue's previous tag.
* `all-vX.Y.Z` publishes the meta-package alone.

A tag must be exactly one step above the previous tag of its package — the next patch, the next minor with
patch 0, or the next major with minor and patch 0 — and the first tag of a package is exactly 1.0.0. The
decision that a change is breaking is made by whoever chooses the number; this script only refuses a number
that cannot have been chosen by that rule.

Writes the versions it settled on as an MSBuild props file (read by build/Packaging.props, so that each
project resolves its OWN version and a ProjectReference becomes a dependency on the right one) and a JSON plan
for the workflow. Policy: ADR-0044 and ADR-0045.
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NS = "DesignPatternCatalog"

# A component is 0 or a number without a leading zero (SemVer item 2), so one release cannot be spelled two ways.
NUMBER = r"(0|[1-9]\d*)"
TAG = re.compile(rf"^(?P<prefix>[a-z0-9]+)-v(?P<major>{NUMBER})\.(?P<minor>{NUMBER})\.(?P<patch>{NUMBER})$")


class PlanError(Exception):
    pass


def discover_packages(repo=REPO):
    """prefix -> project name, from the project folders: Core, the meta-package, and one per catalogue."""
    packages = {}
    for path in sorted(glob.glob(os.path.join(repo, f"{NS}*", f"{NS}*.csproj"))):
        project = os.path.basename(path)[: -len(".csproj")]
        suffix = project[len(NS):].lstrip(".")
        if suffix.startswith("Usage") or suffix == "Tests":
            continue
        packages["all" if suffix == "" else suffix.lower()] = project
    if "core" not in packages or "all" not in packages:
        raise PlanError("expected a Core project and a meta-package project")
    return packages


def parse_tag(tag):
    match = TAG.match(tag)
    if not match:
        raise PlanError(f"'{tag}' is not a release tag: expected <package>-vMAJOR.MINOR.PATCH, e.g. core-v1.0.0")
    return match["prefix"], (int(match["major"]), int(match["minor"]), int(match["patch"]))


def text(version):
    return ".".join(str(part) for part in version)


def bump(version, level):
    major, minor, patch = version
    return {"major": (major + 1, 0, 0), "minor": (major, minor + 1, 0), "patch": (major, minor, patch + 1)}[level]


def level_of(previous, new):
    """The step from previous to new, or an error when it is not exactly one step."""
    for level in ("patch", "minor", "major"):
        if bump(previous, level) == new:
            return level
    raise PlanError(f"{text(new)} is not one step above {text(previous)}: expected {text(bump(previous, 'patch'))}, "
                    f"{text(bump(previous, 'minor'))} or {text(bump(previous, 'major'))}")


def released(tags):
    """prefix -> every version already tagged, ascending."""
    found = {}
    for tag in tags:
        match = TAG.match(tag)
        if match:
            found.setdefault(match["prefix"], []).append(
                (int(match["major"]), int(match["minor"]), int(match["patch"])))
    return {prefix: sorted(versions) for prefix, versions in found.items()}


def plan(tag, tags, packages):
    prefix, version = parse_tag(tag)
    if prefix not in packages:
        raise PlanError(f"'{prefix}' is not a package: expected one of {', '.join(sorted(packages))}")

    history = released(tags)
    # The trigger is itself a tag by the time the workflow runs, so it is set aside: what matters is what the
    # package had BEFORE it. A tag that is not above the latest one is refused rather than read as a first release.
    others = [v for v in history.get(prefix, []) if v != version]
    if others and others[-1] > version:
        raise PlanError(f"{tag} is below the latest release of '{prefix}', {prefix}-v{text(others[-1])}")
    previous = others[-1] if others else None

    if previous is None:
        if version != (1, 0, 0):
            raise PlanError(f"the first release of '{prefix}' is 1.0.0, not {text(version)} (ADR-0045)")
        level = None
    else:
        level = level_of(previous, version)

    # What every package stands at once this release is done: the last tag it has, unless this release moves it.
    last = {p: (history[p][-1] if p in history else None) for p in packages}  # ascending, so [-1] is the latest
    last[prefix] = version
    chosen = {}

    if prefix == "core":
        breaking = level == "major"
        chosen["core"] = version
        for p in packages:
            if p == "core":
                continue
            if last[p] is None:
                chosen[p] = (1, 0, 0)
            else:
                chosen[p] = bump(last[p], "major" if breaking else "patch")
    elif prefix == "all":
        chosen["all"] = version
    else:
        chosen[prefix] = version
        # The meta-package follows the step the tag takes. A catalogue's very first tag gives it a new
        # dependency, which is a minor step.
        step = level or "minor"
        if last["all"] is None:
            raise PlanError("the meta-package has never been released: tag core-v1.0.0 first, which releases "
                            "every package")
        chosen["all"] = bump(last["all"], step)

    last.update(chosen)
    if prefix != "core":
        unreleased = sorted(p for p in packages if last[p] is None)
        if unreleased:
            raise PlanError("the meta-package depends on every package, and these have never been released: "
                            + ", ".join(unreleased) + ". Tag core-v1.0.0 (which releases every package) or "
                            "tag each of them first")

    order = ["core"] + sorted(p for p in packages if p not in ("core", "all")) + ["all"]
    publish = [p for p in order if p in chosen]
    new_tags = [f"{p}-v{text(chosen[p])}" for p in publish if f"{p}-v{text(chosen[p])}" != tag]

    return {
        "trigger": tag,
        "level": level,
        "publish": [{"package": packages[p], "prefix": p, "version": text(chosen[p])} for p in publish],
        "tagsToCreate": new_tags,
        "versions": {packages[p]: text(last[p]) for p in packages if last[p] is not None},
    }


def props(versions):
    """One Version per project, selected by project name so a ProjectReference resolves the right one."""
    lines = ["<Project>",
             "  <!-- Generated by tools/release/plan.py for one release. Never committed (ADR-0044). -->",
             "  <PropertyGroup>"]
    for project, version in sorted(versions.items()):
        lines.append(f"    <Version Condition=\"'$(MSBuildProjectName)' == '{project}'\">{version}</Version>")
    lines += ["  </PropertyGroup>", "</Project>", ""]
    return "\n".join(lines)


def git_tags():
    out = subprocess.run(["git", "tag", "--list"], cwd=REPO, check=True, capture_output=True, text=True)
    return out.stdout.split()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--props", required=True)
    parser.add_argument("--plan", required=True)
    args = parser.parse_args(argv)

    try:
        result = plan(args.tag, git_tags(), discover_packages())
    except PlanError as error:
        print(f"plan: {error}", file=sys.stderr)
        return 1

    with open(args.props, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(props(result["versions"]))
    with open(args.plan, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")

    print(f"{args.tag}: publishes {len(result['publish'])} package(s)")
    for entry in result["publish"]:
        print(f"  {entry['package']} {entry['version']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
