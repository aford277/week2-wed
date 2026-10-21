"""
test_run_stats.py -- Part C: your unit tests for run_stats.py.

Run from the starter_code folder:
    python -m unittest -v test_run_stats

Requirements (see README, Part C):
  * at least 12 test methods
  * one regression test for each of the 7 bugs (a test that FAILS on the buggy file and PASSES once fixed)
  * at least 3 tests of bad or unusual input (empty list, n == 0, missing key)
  * at least 1 test that uses assertRaises
  * at least 1 use of setUp (so tests stay independent) and at least 1 use of assertLogs (Part B)
Name every test for the behaviour it protects, e.g. test_even_count_averages_two_middle_values.
"""
import unittest

import run_stats


class TestMedian(unittest.TestCase):
    # Worked example: Arrange, Act, Assert.
    def test_odd_count_returns_middle(self):
        values = [5, 1, 3]                       # Arrange
        result = run_stats.median(values)        # Act
        self.assertEqual(result, 3)              # Assert

    def test_even_count_returns_mean_of_middle(self):
        values = [6, 4, 3, 2]
        result = run_stats.median(values)
        self.assertEqual(result, 3.5)

    def test_empty_list(self):
        values = []
        with self.assertRaises(ValueError):
            run_stats.median(values)

    def test_input_list_not_changed(self):
        values = [3, 6, 4, 2]
        before = list(values)
        run_stats.median(values)
        self.assertEqual(values, before)


class TestSlowest(unittest.TestCase):
    def test_biggest_comes_first(self):
        values = [200, 300, 100, 400]
        result = run_stats.slowest(values, 5)
        self.assertEqual(result[0], 400)

    def test_n_is_zero(self):
        values = [100, 200, 250]
        result = run_stats.slowest(values, 0)
        self.assertEqual(result, [])

    def test_list_not_reordered(self):
        values = [150, 320, 100, 400, 200]
        before = list(values)
        run_stats.slowest(values, 2)
        self.assertEqual(values, before)


class TestGroupBySuite(unittest.TestCase):

    def setUp(self):
        # every result has a suite (BUG-3)
        self.values = [
            {"test": "t1", "suite": "login",  "status": "pass"},
            {"test": "t2", "suite": "login",  "status": "fail"},
            {"test": "t3", "suite": "login",  "status": "pass"},
            {"test": "t4", "suite": "search", "status": "pass"},
            {"test": "t5", "suite": "search", "status": "skip"},
        ]

        # one result with no "suite" key -> should go to "unknown"
        self.values_missing_suite = [
            {"test": "t1", "suite": "login", "status": "pass"},
            {"test": "t6", "status": "fail"},
        ]
    # TODO: counts per suite and status (BUG-3)    TODO: missing "suite" -> "unknown"    TODO: assertLogs WARNING
    def test_count_per_suite_and_status(self):
        expected = {
            "login":  {"pass": 2, "fail": 1},
            "search": {"pass": 1, "skip": 1},
        }
        result = run_stats.group_by_suite(self.values)
        self.assertEqual(result, expected)

    


class TestNoteFlaky(unittest.TestCase):
    pass
    # TODO: two calls without a list do not share state (BUG-4)    TODO: caller's own list is extended


class TestRunIdAndSummary(unittest.TestCase):
    def setUp(self):
        run_stats.run_counter = 0                # reset shared state so each test starts clean
        self.results = [{"test": "t1", "suite": "login", "status": "pass"}]

    pass
    # TODO: ids increase (BUG-5)    TODO: summary with durations (latest_ms, BUG-6)    TODO: summary with [] (BUG-7)


if __name__ == "__main__":
    unittest.main()
