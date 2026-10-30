import contextlib
import copy
import csv
import io
import json
import unittest

from dprk_fightback.__main__ import load_data, main, validate


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data = load_data()

    def test_seed_is_consistent(self):
        self.assertEqual(validate(self.data), [])

    def test_fee_arithmetic_mismatch_is_rejected(self):
        data = copy.deepcopy(self.data)
        scenario = next(record for record in data["claims"] if record["evidence"] == "calculated")
        scenario["amount"]["values"][0] = "42"
        self.assertTrue(any("do not match" in error for error in validate(data)))

    def test_revenue_context_cannot_be_used_as_attributed_flow(self):
        data = copy.deepcopy(self.data)
        scenario = next(record for record in data["claims"] if record["evidence"] == "calculated")
        scenario["calculation"]["flow_claim"] = "vultisig-all-user-context-revenue"
        self.assertTrue(any("reported flow" in error for error in validate(data)))

    def test_nonfinite_amount_is_rejected(self):
        for value in ["NaN", "Infinity", "-1"]:
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data["claims"][0]["amount"]["value"] = value
                self.assertTrue(validate(data))

    def run_cli(self, args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(args), 0)
        return output.getvalue()

    def test_search_reported_filter_does_not_include_scenarios(self):
        result = json.loads(self.run_cli(["search", "Harmony", "--evidence", "reported", "--json"]))
        self.assertTrue(result["claims"])
        self.assertTrue(all(record["evidence"] == "reported" for record in result["claims"]))

    def test_export_keeps_sources_and_limits(self):
        rows = list(csv.DictReader(io.StringIO(self.run_cli(["export", "--format", "csv", "--service", "vultisig"]))))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["metric"], "context_revenue")
        self.assertIn("unknown", rows[0]["limitations"])
        self.assertTrue(json.loads(rows[0]["sources"])[0]["url"].startswith("https://"))

    def test_unknown_amount_is_not_rendered_as_zero(self):
        output = self.run_cli(["show", "JoinMarket"])
        self.assertIn("Unknown does not mean zero", output)

    def test_fee_output_exposes_assumptions(self):
        output = self.run_cli(["fees", "--service", "exch"])
        self.assertIn("calculated", output)
        self.assertIn("Assumptions:", output)
        self.assertIn("Not observed fee receipts", output)


if __name__ == "__main__":
    unittest.main()
