"""
Career Guidance System - Main Streamlit App
"""

import streamlit as st
import pandas as pd

from recommendation import load_careers, get_recommendations
from skill_gap import load_courses, analyze_gaps
from visualization import plot_career_scores, plot_model_comparison
from report_generator import generate_pdf_report
from advanced_features import get_personality_recommendations, find_similar_careers
from advanced_features import save_user_history, load_user_history

try:
    from models.ml_engine import train_and_compare_models

    ML_AVAILABLE = True
except:
    ML_AVAILABLE = False

st.set_page_config(page_title="Career Guidance", page_icon="💼", layout="wide")

# === SIDEBAR ===
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:",
                        ["🏠 Home", "📝 Assessment", "🎯 Recommendations", "📊 ML Models", "📄 Report"])

# === HOME PAGE ===
if page == "🏠 Home":
    st.title("💼 Career Guidance System")
    st.markdown("### Discover Your Perfect Career Path")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📝 **Take Assessment**\n\nAnswer questions about your skills and interests.")
    with col2:
        st.info("🎯 **Get Recommendations**\n\nSee top career matches.")
    with col3:
        st.info("📚 **Learn Skills**\n\nIdentify gaps and find courses.")

    st.markdown("---")
    st.markdown("### Recent Users")
    history = load_user_history()
    if history:
        for h in history[-5:]:
            st.write(f"- {h['timestamp']}: {h['user'].get('name', 'Anonymous')}")


# === ASSESSMENT PAGE ===
elif page == "📝 Assessment":
    st.title("📝 Career Assessment")
    st.markdown("Please fill in your details:")

    with st.form("assessment_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name")
            age = st.number_input("Age", 16, 60, 22)
            degree = st.selectbox("Degree",
                                  ["High School", "Engineering", "Commerce", "Arts", "Science", "Medicine", "Law",
                                   "Other"])
            personality = st.selectbox("Personality Type",
                                       ["", "INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", "ISTJ",
                                        "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"])

        with col2:
            skills = st.text_input("Skills (comma-separated)", "Python, Excel, SQL")
            interests = st.text_input("Interests (comma-separated)", "Data, Technology")
            preferred_field = st.selectbox("Preferred Field",
                                           ["Technology", "Business", "Healthcare", "Creative Arts", "Education",
                                            "Government", "Sports", "Media", "Science", "Other"])
            work_style = st.selectbox("Work Style", ["Team", "Individual", "Both"])

        submitted = st.form_submit_button("🔍 Get Recommendations")

    if submitted:
        st.session_state['user_data'] = {
            'name': name, 'age': age, 'degree': degree,
            'personality': personality, 'skills': skills,
            'interests': interests, 'preferred_field': preferred_field,
            'work_style': work_style
        }
        st.success("Assessment submitted! Go to Recommendations page.")


# === RECOMMENDATIONS PAGE ===
elif page == "🎯 Recommendations":
    st.title("🎯 Career Recommendations")

    if 'user_data' not in st.session_state:
        st.warning("Please fill the assessment form first!")
    else:
        user_data = st.session_state['user_data']
        careers_df = load_careers()
        courses_df = load_courses()

        recommendations = get_recommendations(user_data, careers_df, top_n=5)

        st.markdown("### Your Top 5 Career Matches")

        for i, rec in enumerate(recommendations, 1):
            with st.expander(f"{i}. {rec['Career']} - {rec['Match Score']}%"):
                st.write(f"**Domain:** {rec['Domain']}")
                st.write(f"**Description:** {rec['Description']}")
                st.write(f"**Matched Skills:** {', '.join(rec['Matched Skills'])}")
                st.write(f"**Required Skills:** {', '.join(rec['Required Skills'])}")

        # Skill Gaps
        skill_gaps = analyze_gaps(recommendations, user_data.get('skills', '').split(','), courses_df)

        st.markdown("### Skill Gap Analysis")
        for gap in skill_gaps:
            with st.expander(f"{gap['Career']} - Missing Skills"):
                st.write(f"**Missing:** {', '.join(gap['Missing Skills'])}")
                st.write(f"**Suggested Courses:** {', '.join(gap['Suggested Courses'])}")

        # Save history
        save_user_history(user_data, recommendations)
        st.success("Recommendations saved to history!")


# === ML MODELS PAGE ===
elif page == "📊 ML Models":
    st.title("📊 Machine Learning Models")
    st.markdown("Training and comparing classification models...")

    if st.button("🚀 Train Models"):
        careers_df = load_careers()
        results, best_model, best_acc = train_and_compare_models(careers_df)

        st.success(f"Best Model: {best_model} ({best_acc:.1%})")

        fig = plot_model_comparison(results)
        st.pyplot(fig)


# === REPORT PAGE ===
elif page == "📄 Report":
    st.title("📄 Generate Report")

    if 'user_data' not in st.session_state:
        st.warning("Please fill the assessment form first!")
    else:
        user_data = st.session_state['user_data']
        careers_df = load_careers()
        courses_df = load_courses()

        recommendations = get_recommendations(user_data, careers_df)
        skill_gaps = analyze_gaps(recommendations, user_data.get('skills', '').split(','), courses_df)

        if st.button("📥 Generate PDF Report"):
            path = generate_pdf_report(user_data, recommendations, skill_gaps)
            st.success(f"Report saved: {path}")

            with open(path, "rb") as file:
                st.download_button("Download Report", file, file_name="career_report.pdf")