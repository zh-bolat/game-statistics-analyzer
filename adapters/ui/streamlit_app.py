import json
import pandas as pd
import streamlit as st

from core.models import GameRecord
from core.services import StatsAnalyzer


def _parse_uploaded_file(uploaded_file) -> list[GameRecord]:
    records = []
    raw_data = json.load(uploaded_file)

    for entry in raw_data:
        try:
            records.append(
                GameRecord(
                    player=entry["player"],
                    score=entry["score"],
                    date=entry["date"],
                )
            )
        except (KeyError, ValueError, TypeError) as e:
            st.warning(f"Запись пропущена: {entry} — Причина: {e}")

    return records


@st.cache_data
def convert_leaderboard_to_csv(leaderboard_list):
    df = pd.DataFrame(leaderboard_list, columns=["Игрок", "Макс. счёт"])
    return df.to_csv(index=False).encode("utf-8")


def convert_leaderboard_to_json(leaderboard_list):
    df = pd.DataFrame(leaderboard_list, columns=["Игрок", "Макс. счёт"])
    return df.to_json(orient="records", force_ascii=False, indent=4)


def run():
    st.set_page_config(
        page_title="Анализатор игровой статистики",
        page_icon="🎮",
        layout="wide",
    )

    st.title("Анализатор игровой статистики")
    st.markdown(
        "Загрузите JSON-файл с игровыми сессиями для получения аналитики."
    )

    uploaded_file = st.file_uploader(
        label="Перетащите или выберите файл", type=["json"]
    )

    if uploaded_file is None:
        st.info("Ожидание файла...")
        return

    records = _parse_uploaded_file(uploaded_file)

    if not records:
        st.error("Файл не содержит корректных записей.")
        return

    analyzer = StatsAnalyzer(iter(records))

    st.success(f"Загружено записей: {len(records)}")

    st.markdown("---")
    st.subheader("Ключевые показатели")

    records_data = analyzer.get_records()
    all_time = records_data["absolute_record"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Всего записей", len(records))
    col2.metric("Абсолютный рекорд", all_time["score"] if all_time else "—")
    col3.metric("Лучший игрок", all_time["player"] if all_time else "—")

    st.markdown("---")
    st.subheader("Глобальный лидерборд")

    leaderboard = analyzer.get_leaderboard()
    leaderboard_data = {
        "Игрок": [p for p, _ in leaderboard],
        "Макс. счёт": [s for _, s in leaderboard],
    }
    st.dataframe(leaderboard_data, use_container_width=True)

    st.markdown("---")
    st.subheader("Средний счёт игроков")

    averages = analyzer.get_average_scores()
    averages_data = {
        "Игрок": [p for p, _ in averages],
        "Средний счёт": [round(a, 2) for _, a in averages],
    }
    st.dataframe(averages_data, use_container_width=True)

    st.markdown("---")
    st.subheader("Лучшие результаты по дням")

    daily_best = records_data["daily_best"]
    if daily_best:
        st.line_chart(daily_best
