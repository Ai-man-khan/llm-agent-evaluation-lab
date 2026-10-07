from pathlib import Path
import unittest

from evaluator.controls import run_control_matrix
from evaluator.runner import evaluate_candidate


ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "examples" / "synthetic-lease-registry"


class EvaluatorTests(unittest.TestCase):
    def test_reference_passes(self):
        result = evaluate_candidate(TASK / "reference", TASK / "grader")
        self.assertTrue(result.passed, result.stderr)

    def test_starter_fails(self):
        result = evaluate_candidate(TASK / "workspace", TASK / "grader")
        self.assertFalse(result.passed)

    def test_no_op_fails(self):
        result = evaluate_candidate(TASK / "no_op", TASK / "grader")
        self.assertFalse(result.passed)

    def test_control_matrix_is_healthy(self):
        matrix = run_control_matrix(TASK)
        self.assertTrue(matrix["reference"].passed)
        self.assertFalse(matrix["starter"].passed)
        self.assertFalse(matrix["no-op"].passed)


if __name__ == "__main__":
    unittest.main()
