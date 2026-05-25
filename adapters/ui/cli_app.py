from core.services import StatsAnalyzer

class CLIAdapter:

    def init(self, analyzer: StatsAnalyzer):
        self._analyzer = analyzer

    def run(self):
        print("\n" + "=" * 50)
        print("       АНАЛИЗАТОР ИГРОВОЙ СТАТИСТИКИ")
        print("=" * 50)

        self._print_leaderboard()
        self._print_averages()
        self._print_records()

    def _print_leaderboard(self):
        print("\n ГЛОБАЛЬНЫЙ ЛИДЕРБОРД (макс. счёт)")
        print("-" * 35)

        leaderboard = self._analyzer.get_leaderboard()

        if not leaderboard:
            print("  Нет данных.")
            return

        for rank, (player, score) in enumerate(leaderboard, start=1):
            print(f"  {rank:>2}. {player:<20} {score:>6} очков")

    def _print_averages(self):
        print("\n СРЕДНИЙ СЧЁТ ИГРОКОВ")
        print("-" * 35)

        averages = self._analyzer.get_average_scores()

        if not averages:
            print("  Нет данных.")
            return

        for player, avg in averages:
            print(f"  {player:<20} {avg:>8.2f} очков")

    def _print_records(self):
        print("\n РЕКОРДЫ")
        print("-" * 35)

        records = self._analyzer.get_records()

        all_time = records["all_time_best"]
        if all_time:
            print(f"  Абсолютный рекорд: {all_time.player} — {all_time.score} очков ({all_time.date})")
        else:
            print("  Нет данных.")
            return

        print("\n  Лучшие результаты по дням:")
        for date, record in records["daily_best"].items():
            print(f"    {date}: {record.player} — {record.score} очков")

        print("\n" + "=" * 50)
