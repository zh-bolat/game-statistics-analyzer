import unittest

from core.models import GameRecord
from core.services import StatsAnalyzer


class TestGameRecordValidation(unittest.TestCase):

    def test_valid_record(self):
        record = GameRecord(player="Alice", score=100, date="2024-01-15")
        self.assertEqual(record.player, "Alice")
        self.assertEqual(record.score, 100)
        self.assertEqual(record.date, "2024-01-15")

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            GameRecord(player="Alice", score=100, date="15-01-2024")

    def test_invalid_date_slash(self):
        with self.assertRaises(ValueError):
            GameRecord(player="Alice", score=100, date="2024/01/15")

    def test_invalid_date_empty(self):
        with self.assertRaises(ValueError):
            GameRecord(player="Alice", score=100, date="")

    def test_negative_score(self):
        with self.assertRaises(ValueError):
            GameRecord(player="Alice", score=-1, date="2024-01-15")

    def test_boolean_score_rejected(self):
        with self.assertRaises(ValueError):
            GameRecord(player="Alice", score=True, date="2024-01-15")

    def test_empty_player_name(self):
        with self.assertRaises(ValueError):
            GameRecord(player="", score=100, date="2024-01-15")

    def test_whitespace_player_name(self):
        with self.assertRaises(ValueError):
            GameRecord(player="   ", score=100, date="2024-01-15")

    def test_zero_score_is_valid(self):
        record = GameRecord(player="Alice", score=0, date="2024-01-15")
        self.assertEqual(record.score, 0)


class TestStatsAnalyzerEmpty(unittest.TestCase):

    def setUp(self):
        self.analyzer = StatsAnalyzer(iter([]))

    def test_leaderboard_empty(self):
        result = self.analyzer.get_leaderboard()
        self.assertEqual(result, [])

    def test_averages_empty(self):
        result = self.analyzer.get_average_scores()
        self.assertEqual(result, [])

    def test_records_empty(self):
        result = self.analyzer.get_records()
        self.assertIsNone(result["absolute_record"])
        self.assertEqual(result["daily_best"], {})


class TestStatsAnalyzerLogic(unittest.TestCase):

    def setUp(self):
        records = [
            GameRecord(player="Alice", score=300, date="2024-01-01"),
            GameRecord(player="Alice", score=100, date="2024-01-02"),
            GameRecord(player="Bob",   score=200, date="2024-01-01"),
            GameRecord(player="Bob",   score=400, date="2024-01-02"),
            GameRecord(player="Carol", score=150, date="2024-01-01"),
        ]
        self.analyzer = StatsAnalyzer(iter(records))

    def test_leaderboard_order(self):
        leaderboard = self.analyzer.get_leaderboard()
        players = [p for p, _ in leaderboard]
        self.assertEqual(players, ["Bob", "Alice", "Carol"])

    def test_leaderboard_max_score(self):
        leaderboard = dict(self.analyzer.get_leaderboard())
        self.assertEqual(leaderboard["Alice"], 300)
        self.assertEqual(leaderboard["Bob"], 400)

    def test_average_scores(self):
        averages = dict(self.analyzer.get_average_scores())
        self.assertAlmostEqual(averages["Alice"], 200.0)
        self.assertAlmostEqual(averages["Bob"], 300.0)
        self.assertAlmostEqual(averages["Carol"], 150.0)

    def test_all_time_best(self):
        records = self.analyzer.get_records()
        best = records["absolute_record"]
        self.assertEqual(best["player"], "Bob")
        self.assertEqual(best["score"], 400)

    def test_daily_best(self):
        records = self.analyzer.get_records()
        daily = records["daily_best"]
        self.assertEqual(daily["2024-01-01"], 300)
        self.assertEqual(daily["2024-01-02"], 400)


class TestStatsAnalyzerSingleRecord(unittest.TestCase):

    def setUp(self):
        records = [GameRecord(player="Solo", score=999, date="2024-06-01")]
        self.analyzer = StatsAnalyzer(iter(records))

    def test_leaderboard_single(self):
        leaderboard = self.analyzer.get_leaderboard()
        self.assertEqual(len(leaderboard), 1)
        self.assertEqual(leaderboard[0], ("Solo", 999))

    def test_average_single(self):
        averages = dict(self.analyzer.get_average_scores())
        self.assertAlmostEqual(averages["Solo"], 999.0)

    def test_all_time_best_single(self):
        records = self.analyzer.get_records()
        self.assertEqual(records["absolute_record"]["player"], "Solo")


class TestStatsAnalyzerDuplicates(unittest.TestCase):

    def setUp(self):
        records = [
            GameRecord(player="Alice", score=50,  date="2024-03-01"),
            GameRecord(player="Alice", score=50,  date="2024-03-02"),
            GameRecord(player="Alice", score=50,  date="2024-03-03"),
        ]
        self.analyzer = StatsAnalyzer(iter(records))

    def test_leaderboard_no_duplicates(self):
        leaderboard = self.analyzer.get_leaderboard()
        self.assertEqual(len(leaderboard), 1)

    def test_average_equal_scores(self):
        averages = dict(self.analyzer.get_average_scores())
        self.assertAlmostEqual(averages["Alice"], 50.0)


if __name__ == "__main__":
    unittest.main()
