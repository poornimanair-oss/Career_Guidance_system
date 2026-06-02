"""
Advanced Features Module
======================
- Resume parsing
- Personality-based recommendations
- Career similarity search
- User history saving
"""

import os
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# === PERSONALITY-BASED RECOMMENDATIONS ===
PERSONALITY_CAREER_MAP = {
    "INTJ": ["Data Scientist", "Software Developer", "Architect"],
    "INTP": ["Data Scientist", "ML Engineer", "Researcher"],
    "ENTJ": ["Entrepreneur", "Marketing Manager", "CEO"],
    "ENTP": ["Content Creator", "Journalist", "Entrepreneur"],
    "INFJ": ["Psychologist", "Teacher", "Professor"],
    "INFP": ["Writer", "Graphic Designer", "Musician"],
    "ENFJ": ["Teacher", "HR Manager", "Marketing Manager"],
    "ENFP": ["Actor", "Content Creator", "Journalist"],
    "ISTJ": ["Accountant", "Lawyer", "Civil Servant"],
    "ISFJ": ["Nurse", "Teacher", "Social Worker"],
    "ESTJ": ["Manager", "Business Analyst", "IAS Officer"],
    "ESFJ": ["Nurse", "Teacher", "HR Manager"],
    "ISTP": ["Engineer", "Cybersecurity Analyst", "Chef"],
    "ISFP": ["Photographer", "Graphic Designer", "Dancer"],
    "ESTP": ["Sales Manager", "Entrepreneur", "Athlete"],
    "ESFP": ["Actor", "Content Creator", "Fitness Trainer"]
}


def get_personality_recommendations(personality_type):
    """Get careers based on personality type (MBTI)."""
    p_type = personality_type.upper().strip()
    return PERSONALITY_CAREER_MAP.get(p_type, ["General careers"])


# === CAREER SIMILARITY SEARCH ===
def find_similar_careers(target_career, careers_df, top_n=5):
    """Find similar careers using TF-IDF and cosine similarity."""
    careers_df = careers_df.copy()
    careers_df['combined'] = (careers_df['Required Skills'].astype(str) + " " +
                              careers_df['Interests'].astype(str))

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(careers_df['combined'])

    try:
        target_idx = careers_df[careers_df['Career Name'] == target_career].index[0]
    except IndexError:
        return []

    cosine_sim = cosine_similarity(tfidf_matrix[target_idx], tfidf_matrix).flatten()
    sim_scores = sorted(enumerate(cosine_sim), key=lambda x: x[1], reverse=True)
    sim_scores = [s for s in sim_scores if s[0] != target_idx]

    similar = []
    for idx, score in sim_scores[:top_n]:
        row = careers_df.iloc[idx]
        similar.append({
            "Career": row['Career Name'],
            "Similarity Score": round(score * 100, 2),
            "Domain": row['Domain']
        })

    return similar


# === USER HISTORY ===
HISTORY_FILE = "user_history.json"


def save_user_history(user_data, recommendations):
    """Save user session to JSON file."""
    entry = {
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_data,
        "recommendations": [{r['Career']: r['Match Score']} for r in recommendations]
    }

    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        except:
            history = []

    history.append(entry)

    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

    return HISTORY_FILE


def load_user_history():
    """Load past user sessions."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []


if __name__ == "__main__":
    # Test
    print(get_personality_recommendations("INTJ"))