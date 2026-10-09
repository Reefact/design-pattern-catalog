#!/usr/bin/env python3
"""Tests for the release planner:  python3 -m unittest discover -s tools/release"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan as release  # noqa: E402

PACKAGES = {
    "core": "DesignPatternCatalog.Core",
    "all": "DesignPatternCatalog",
    "gangoffour": "DesignPatternCatalog.GangOfFour",
    "reefact": "DesignPatternCatalog.Reefact",
}
FIRST = ["core-v1.0.0", "gangoffour-v1.0.0", "reefact-v1.0.0", "all-v1.0.0"]


def versions_of(result):
    return {entry["prefix"]: entry["version"] for entry in result["publish"]}


class FirstRelease(unittest.TestCase):
    def test_core_releases_every_package_at_one_zero_zero(self):
        result = release.plan("core-v1.0.0", ["core-v1.0.0"], PACKAGES)

        self.assertEqual({"core": "1.0.0", "gangoffour": "1.0.0", "reefact": "1.0.0", "all": "1.0.0"}, versions_of(result))
        self.assertEqual(["core", "gangoffour", "reefact", "all"], [e["prefix"] for e in result["publish"]])
        self.assertEqual(["gangoffour-v1.0.0", "reefact-v1.0.0", "all-v1.0.0"], result["tagsToCreate"])

    def test_the_first_tag_of_a_package_is_exactly_one_zero_zero(self):
        for tag in ("core-v0.9.0", "core-v1.0.1", "core-v2.0.0"):
            with self.assertRaises(release.PlanError, msg=tag):
                release.plan(tag, [tag], PACKAGES)

    def test_a_catalogue_cannot_start_the_release_while_the_meta_package_does_not_exist(self):
        with self.assertRaises(release.PlanError):
            release.plan("reefact-v1.0.0", ["reefact-v1.0.0"], PACKAGES)


class CoreCascade(unittest.TestCase):
    def test_a_non_breaking_core_moves_everyone_one_patch(self):
        tags = FIRST + ["reefact-v1.2.0", "core-v1.0.1"]
        result = release.plan("core-v1.0.1", tags, PACKAGES)

        self.assertEqual({"core": "1.0.1", "gangoffour": "1.0.1", "reefact": "1.2.1", "all": "1.0.1"}, versions_of(result))

    def test_a_core_minor_is_not_breaking(self):
        result = release.plan("core-v1.1.0", FIRST + ["core-v1.1.0"], PACKAGES)

        self.assertEqual("1.0.1", versions_of(result)["reefact"])

    def test_a_core_major_moves_everyone_to_the_next_major(self):
        tags = FIRST + ["reefact-v1.2.0", "core-v2.0.0"]
        result = release.plan("core-v2.0.0", tags, PACKAGES)

        self.assertEqual({"core": "2.0.0", "gangoffour": "2.0.0", "reefact": "2.0.0", "all": "2.0.0"}, versions_of(result))

    def test_a_package_added_since_gets_one_zero_zero_in_the_cascade(self):
        tags = ["core-v1.0.0", "gangoffour-v1.0.0", "all-v1.0.0", "core-v1.0.1"]
        result = release.plan("core-v1.0.1", tags, PACKAGES)

        self.assertEqual("1.0.0", versions_of(result)["reefact"])
        self.assertEqual("1.0.1", versions_of(result)["gangoffour"])


class CatalogueTag(unittest.TestCase):
    def test_a_catalogue_patch_gives_the_meta_package_a_patch(self):
        result = release.plan("reefact-v1.0.1", FIRST + ["reefact-v1.0.1"], PACKAGES)

        self.assertEqual({"reefact": "1.0.1", "all": "1.0.1"}, versions_of(result))
        self.assertEqual(["all-v1.0.1"], result["tagsToCreate"])

    def test_a_catalogue_minor_gives_the_meta_package_a_minor(self):
        result = release.plan("reefact-v1.1.0", FIRST + ["reefact-v1.1.0"], PACKAGES)

        self.assertEqual("1.1.0", versions_of(result)["all"])

    def test_a_catalogue_major_gives_the_meta_package_a_major(self):
        result = release.plan("reefact-v2.0.0", FIRST + ["reefact-v2.0.0"], PACKAGES)

        self.assertEqual("2.0.0", versions_of(result)["all"])

    def test_packages_left_alone_keep_the_version_they_were_released_at(self):
        tags = FIRST + ["gangoffour-v1.4.0", "reefact-v1.0.1"]
        result = release.plan("reefact-v1.0.1", tags, PACKAGES)

        self.assertEqual("1.4.0", result["versions"]["DesignPatternCatalog.GangOfFour"])
        self.assertEqual("1.0.0", result["versions"]["DesignPatternCatalog.Core"])

    def test_a_catalogue_never_released_blocks_the_meta_package(self):
        tags = ["core-v1.0.0", "gangoffour-v1.0.0", "all-v1.0.0", "gangoffour-v1.0.1"]

        with self.assertRaises(release.PlanError) as raised:
            release.plan("gangoffour-v1.0.1", tags, PACKAGES)
        self.assertIn("reefact", str(raised.exception))


class TagMeta(unittest.TestCase):
    def test_the_meta_package_can_be_released_alone(self):
        result = release.plan("all-v1.0.1", FIRST + ["all-v1.0.1"], PACKAGES)

        self.assertEqual({"all": "1.0.1"}, versions_of(result))
        self.assertEqual([], result["tagsToCreate"])


class Refusals(unittest.TestCase):
    def test_a_jump_is_refused(self):
        with self.assertRaises(release.PlanError):
            release.plan("core-v1.0.3", FIRST + ["core-v1.0.3"], PACKAGES)

    def test_a_step_back_is_refused(self):
        with self.assertRaises(release.PlanError):
            release.plan("core-v1.0.0", FIRST + ["core-v1.0.1"], PACKAGES)

    def test_a_minor_step_must_reset_the_patch(self):
        with self.assertRaises(release.PlanError):
            release.plan("core-v1.1.1", FIRST + ["core-v1.1.1"], PACKAGES)

    def test_an_unknown_package_is_refused(self):
        with self.assertRaises(release.PlanError):
            release.plan("nonesuch-v1.0.0", FIRST + ["nonesuch-v1.0.0"], PACKAGES)

    def test_a_pre_release_or_a_malformed_tag_is_refused(self):
        for tag in ("core-v1.0.0-rc1", "core-1.0.0", "v1.0.0", "Core-v1.0.0", "core-v01.0.0", "core-v1.00.0", "core-v1.0.00"):
            with self.assertRaises(release.PlanError, msg=tag):
                release.parse_tag(tag)


class Props(unittest.TestCase):
    def test_each_project_gets_its_own_version_selected_by_name(self):
        text = release.props({"DesignPatternCatalog.Core": "1.0.1", "DesignPatternCatalog": "1.2.0"})

        self.assertIn("'$(MSBuildProjectName)' == 'DesignPatternCatalog.Core'\">1.0.1<", text)
        self.assertIn("'$(MSBuildProjectName)' == 'DesignPatternCatalog'\">1.2.0<", text)


class Discovery(unittest.TestCase):
    def test_the_real_repository_has_core_the_meta_package_and_the_catalogues(self):
        packages = release.discover_packages()

        self.assertEqual("DesignPatternCatalog.Core", packages["core"])
        self.assertEqual("DesignPatternCatalog", packages["all"])
        self.assertEqual("DesignPatternCatalog.Reefact", packages["reefact"])
        self.assertEqual(14, len(packages))
        self.assertFalse([p for p in packages if "usage" in p or "tests" in p])


if __name__ == "__main__":
    unittest.main()
