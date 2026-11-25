from pathlib import Path
import csv, json, math, unittest
from score_raps26 import score_records
ROOT = Path(__file__).resolve().parent

class ScoreTests(unittest.TestCase):
    def setUp(self):
        with (ROOT / "synthetic_input.csv").open() as f:
            self.records = list(csv.DictReader(f))
        self.constants = json.loads((ROOT / "RAPS26_constants.json").read_text())

    def test_expected_and_equivalent_formula(self):
        with (ROOT / "synthetic_expected_output.csv").open() as f:
            expected = list(csv.DictReader(f))
        actual = score_records(self.records, "cerebellar_cortex")
        self.assertEqual(len(actual), len(expected))
        for row, result, target in zip(self.records, actual, expected):
            for key in ["RAPS_raw", "RAPS_z"]:
                self.assertAlmostEqual(result[key], float(target[key]), delta=1e-12)
            direct = self.constants["raw_intercept"] + math.fsum(
                b * float(row[r]) for r, b in zip(
                    self.constants["regions"], self.constants["coefficients_raw_ROI"]))
            self.assertAlmostEqual(result["RAPS_raw"], direct, delta=1e-12)

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            score_records(self.records, "whole_cerebellum")
        region = self.constants["regions"][0]
        for value in ["nan", "inf", "0", "-1", ""]:
            row = dict(self.records[0]); row[region] = value
            with self.assertRaises(ValueError):
                score_records([row], "cerebellar_cortex")
        row = dict(self.records[0]); del row[region]
        with self.assertRaises(ValueError):
            score_records([row], "cerebellar_cortex")

if __name__ == "__main__":
    unittest.main()
