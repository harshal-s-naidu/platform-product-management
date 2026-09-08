"""Meaningful malformed-data and stale-update checks; no live state edits."""

from copy import deepcopy
from pathlib import Path
import unittest

from validate_state import load_json, validate

ROOT = Path(__file__).resolve().parents[1]


class StateTests(unittest.TestCase):
    def setUp(self):
        self.state = load_json(ROOT / "examples/sample-state.json")

    def assert_invalid(self, text):
        errors, _ = validate(self.state)
        self.assertTrue(any(text in e for e in errors), errors)

    def test_empty_and_sample_are_valid(self):
        self.assertEqual(validate(self.state), ([], []))
        self.assertEqual(validate(load_json(ROOT / "data/state.json")), ([], []))

    def test_missing_required_outcome(self):
        del self.state["use_cases"][0]["attributes"]["outcome"]
        self.assert_invalid("missing outcome")

    def test_duplicate_ids(self):
        self.state["use_cases"].append(deepcopy(self.state["use_cases"][0]))
        self.assert_invalid("Duplicate record IDs")

    def test_dangling_link(self):
        self.state["roadmap_items"][0]["attributes"]["use_case_ids"].append("UC-999")
        self.assert_invalid("dangling reference")

    def test_reference_type(self):
        self.state["roadmap_items"][0]["attributes"]["metric_ids"] = ["UC-001"]
        self.assert_invalid("wrong reference type")

    def test_invalid_calendar_date(self):
        self.state["evidence"][0]["attributes"]["observed_on"] = "2026-02-30"
        self.assert_invalid("invalid date")

    def test_boolean_is_not_record_version(self):
        self.state["use_cases"][0]["record_version"] = True
        self.assert_invalid("expected integer")

    def test_forecast_needs_kind_and_source(self):
        self.state["roadmap_items"][0]["attributes"]["date"] = "2026-02-01"
        self.assert_invalid("date requires kind and source")

    def test_adoption_requires_authority_record(self):
        self.state["decisions"][0]["status"] = "adopted"
        self.assert_invalid("needs owner, choice and date")

    def test_choice_must_be_an_option(self):
        self.state["decisions"][1]["attributes"]["chosen_option"] = "Unconsidered alternative"
        self.assert_invalid("not among options")

    def test_provisional_decision_needs_trigger(self):
        del self.state["decisions"][1]["attributes"]["revisit_trigger"]
        self.assert_invalid("needs revisit trigger")

    def test_risk_acceptance_requires_basis(self):
        self.state["risks"][0]["status"] = "accepted"
        self.assert_invalid("requires basis")

    def test_self_dependency(self):
        self.state["dependencies"][1]["attributes"]["prerequisite_id"] = "UC-001"
        self.assert_invalid("self dependency")

    def test_cycle_is_visible_but_can_be_recorded(self):
        dep = deepcopy(self.state["dependencies"][1])
        dep["id"] = "DEP-003"
        dep["attributes"]["dependent_id"] = "CAP-002"
        dep["attributes"]["prerequisite_id"] = "UC-001"
        self.state["dependencies"].append(dep)
        errors, warnings = validate(self.state)
        self.assertEqual(errors, [])
        self.assertTrue(any("no feasible linear sequence" in w for w in warnings))

    def test_hypothesized_edge_is_not_confirmed_cycle(self):
        dep = deepcopy(self.state["dependencies"][1])
        dep["id"] = "DEP-003"
        dep["status"] = "hypothesized"
        dep["attributes"]["dependent_id"] = "CAP-002"
        dep["attributes"]["prerequisite_id"] = "UC-001"
        self.state["dependencies"].append(dep)
        self.assertEqual(validate(self.state), ([], []))

    def test_unknown_field_fails(self):
        self.state["capabilities"][0]["attributes"]["made_up_score"] = 99
        self.assert_invalid("unknown property")

    def test_missing_baseline_is_preserved(self):
        self.assertNotIn("baseline", self.state["metrics"][0]["attributes"])
        original = deepcopy(self.state)
        validate(self.state)
        self.assertEqual(self.state, original)

    def test_correct_update_and_stale_version(self):
        prior = deepcopy(self.state)
        self.state["state_revision"] += 1
        item = self.state["roadmap_items"][0]
        item["attributes"]["horizon"] = "next"
        item["record_version"] += 1
        self.assertEqual(validate(self.state, prior), ([], []))
        item["record_version"] -= 1
        self.assertTrue(any("version must advance" in e for e in validate(self.state, prior)[0]))

    def test_stale_store_and_revision(self):
        prior = deepcopy(self.state)
        self.state["store_id"] = "another-store"
        errors, _ = validate(self.state, prior)
        self.assertTrue(any("Store identity changed" in e for e in errors))
        self.assertTrue(any("revision must advance" in e for e in errors))

    def test_predecessor_must_be_superseded(self):
        self.state["decisions"][1]["attributes"]["supersedes_id"] = "DEC-001"
        self.assert_invalid("predecessor status not updated")

    def test_duplicate_consumer_link(self):
        link = deepcopy(self.state["use_case_capabilities"][0])
        link["id"] = "LNK-004"
        self.state["use_case_capabilities"].append(link)
        self.assert_invalid("Duplicate use-case/capability")


if __name__ == "__main__":
    unittest.main()
