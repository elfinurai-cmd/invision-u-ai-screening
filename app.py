# app.py

import streamlit as st
import pandas as pd
from scoring import calculate_candidate_score

st.set_page_config(page_title="inVision U Candidate Screening", layout="wide")

st.title("AI Assistant for inVision U Admissions")
st.write("Прототип системы первичного отбора кандидатов")

tab1, tab2 = st.tabs(["Один кандидат", "CSV список кандидатов"])

with tab1:
    st.subheader("Форма кандидата")

    candidate = {
        "candidate_id": st.text_input("ID кандидата"),
        "full_name": st.text_input("ФИО"),
        "age": st.number_input("Возраст", min_value=14, max_value=30, value=17),
        "city": st.text_input("Город"),
        "school_or_college": st.text_input("Школа / колледж"),
        "achievements": st.text_area("Достижения"),
        "leadership_experience": st.text_area("Опыт лидерства"),
        "volunteering": st.text_area("Волонтерство / инициативы"),
        "motivation_text": st.text_area("Почему вы хотите учиться в inVision U?"),
        "growth_story": st.text_area("Опишите трудность, которую вы преодолели, и чему это вас научило"),
        "future_goals": st.text_area("Какие цели вы хотите достичь в будущем?"),
        "essay_text": st.text_area("Эссе")
    }

    if st.button("Оценить кандидата"):
        result = calculate_candidate_score(candidate)

        st.success(f"Итоговый балл: {result['final_score']}")
        st.info(f"Рекомендация: {result['recommendation']}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Leadership", result["leadership"])
        col2.metric("Growth", result["growth"])
        col3.metric("Motivation", result["motivation"])

        col4, col5 = st.columns(2)
        col4.metric("Initiative", result["initiative"])
        col5.metric("Clarity", result["clarity"])

        st.subheader("Объяснение")
        st.write(result["explanation"])

        st.subheader("Важно")
        st.caption("Это вспомогательный инструмент для комиссии. Финальное решение принимает человек.")

with tab2:
    st.subheader("Загрузка CSV")

    uploaded_file = st.file_uploader("Загрузите CSV с кандидатами", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        results = []
        for _, row in df.iterrows():
            candidate_dict = row.to_dict()
            score = calculate_candidate_score(candidate_dict)
            results.append({**candidate_dict, **score})

        result_df = pd.DataFrame(results)
        result_df = result_df.sort_values(by="final_score", ascending=False)

        st.dataframe(result_df, use_container_width=True)

        shortlist = result_df[result_df["recommendation"] == "Shortlist"]
        st.subheader("Shortlist")
        st.dataframe(shortlist, use_container_width=True)