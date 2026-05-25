import json
import os
import pandas as pd
import streamlit as st

from core.models import GameRecord
from core.services import StatsAnalyzer


def _parse_uploaded_file(file_obj) -> list[GameRecord]:
    """Парсит JSON-данные из файлового объекта (uploaded_file или обычный open())."""
    records = []
    try:
        raw_data = json.load(file_obj)
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
    except json.JSONDecodeError:
        st.error("Ошибка чтения JSON: неверный формат файла.")
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
        "Приложение автоматически отображает статистику из системы. Также вы можете загрузить кастомный JSON-файл."
    )

    # Компонент загрузки файлов
    uploaded_file = st.file_uploader(
        label="Перетащите или выберите файл для анализа новой статистики", type=["json"]
    )

    records = []

    # Умный подхват данных: приоритет у загруженного файла, иначе берем системный stats.json
    if uploaded_file is not None:
        records = _parse_uploaded_file(uploaded_file)
    else:
        default_path = "data/stats.json"
        if os.path.exists(default_path):
            with open(default_path, "r", encoding="utf-8") as f:
                records = _parse_uploaded_file(f)
        else:
            st.info("Ожидание загрузки файла (дефолтный файл data/stats.json не найден в системе)...")
            return

    if not records:
        st.error("Не удалось загрузить ни одной корректной игровой записи.")
        return

    # Инициализируем анализатор бизнес-логики
    analyzer = StatsAnalyzer(iter(records))

    st.success(f"Успешно обработано записей: {len(records)}")

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
        # Преобразуем ключи-даты в нормальный формат для линейного графика Streamlit
        chart_data = pd.DataFrame(
            list(daily_best.items()), columns=["Дата", "Лучший счёт"]
        ).set_index("Дата")
        st.line_chart(chart_data)
    else:
        st.info("Нет данных для отображения графика.")


if name == "main":
    run()
