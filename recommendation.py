"""
Career Recommendation Engine
==========================
Matches user profile with career database
Calculates match percentage based on skills and interests
"""

import pandas as pd
import numpy as np


# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_careers(filepath='data/careers.csv'):
    """
    Load careers dataset from CSV file.

    Args:
        filepath: Path to careers.csv

    Returns:
        DataFrame with career data
    """
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return pd.DataFrame()


# ============================================================================
# MATCHING FUNCTIONS
# ============================================================================

def calculate_match_percentage(user_skills, user_interests, career_skills, career_interests):
    """
    Calculate match percentage between user and career.

    Scoring Weights:
    - Skills: 60%
    - Interests: 40%

    Args:
        user_skills: List of user skills
        user_interests: List of user interests
        career_skills: List of career required skills
        career_interests: List of career interests

    Returns:
        Dictionary with score and matched items
    """
    # Convert to sets (lowercase) for comparison
    user_skills_set = set([s.strip().lower() for s in user_skills])
    user_interests_set = set([i.strip().lower() for i in user_interests])
    career_skills_set = set([s.strip().lower() for s in career_skills])
    career_interests_set = set([i.strip().lower() for i in career_interests])

    # Calculate Skill Match (60% weight)
    if len(career_skills_set) > 0:
        skill_matches = user_skills_set.intersection(career_skills_set)
        skill_score = (len(skill_matches) / len(career_skills_set)) * 100
    else:
        skill_score = 0
        skill_matches = set()

    # Calculate Interest Match (40% weight)
    if len(career_interests_set) > 0:
        interest_matches = user_interests_set.intersection(career_interests_set)
        interest_score = (len(interest_matches) / len(career_interests_set)) * 100
    else:
        interest_score = 0
        interest_matches = set()

    # Overall weighted score
    overall_score = (skill_score * 0.6) + (interest_score * 0.4)

    return {
        'score': round(overall_score, 2),
        'matched_skills': list(skill_matches),
        'matched_interests': list(interest_matches)
    }


# ============================================================================
# MAIN RECOMMENDATION FUNCTION
# ============================================================================

def get_recommendations(user_data, careers_df, top_n=5):
    """
    Get top N career recommendations based on user profile.

    Args:
        user_data: Dictionary with user information
        careers_df: DataFrame with career database
        top_n: Number of recommendations to return

    Returns:
        List of career recommendations with match scores
    """
    recommendations = []

    # Extract user inputs
    user_skills = user_data.get('skills', [])
    if isinstance(user_skills, str):
        user_skills = [s.strip() for s in user_skills.split(',')]

    user_interests = user_data.get('interests', [])
    if isinstance(user_interests, str):
        user_interests = [i.strip() for i in user_interests.split(',')]

    user_degree = user_data.get('degree', '').lower()
    preferred_field = user_data.get('preferred_field', '').lower()

    # Score each career in the database
    for index, row in careers_df.iterrows():
        # Get career attributes
        career_skills = str(row['Required Skills']).split(',')
        career_interests = str(row['Interests']).split(',')

        # Calculate base match
        match_result = calculate_match_percentage(
            user_skills,
            user_interests,
            career_skills,
            career_interests
        )

        score = match_result['score']

        # ========== BONUS POINTS ==========

        # Bonus for preferred field (+10 points)
        if preferred_field and preferred_field in row['Domain'].lower():
            score += 10

        # Education relevance bonus (+5 points)
        if user_degree and user_degree in str(row['Education Requirement']).lower():
            score += 5

        # Cap score at 100
        score = min(score, 100)

        # Build recommendation object
        recommendations.append({
            'Career': row['Career Name'],
            'Domain': row['Domain'],
            'Description': row['Description'],
            'Match Score': score,
            'Matched Skills': match_result['matched_skills'],
            'Required Skills': [s.strip() for s in career_skills],
            'Education': row['Education Requirement']
        })

    # Sort by match score (highest first) and return top N
    recommendations = sorted(recommendations, key=lambda x: x['Match Score'], reverse=True)

    return recommendations[:top_n]


# ============================================================================
# TEST FUNCTION
# ============================================================================

if __name__ == "__main__":
    # Test with sample data
    df = load_careers()
    print(f"Loaded {len(df)} careers\n")

    test_user = {
        'name': 'John Doe',
        'skills': 'Python,SQL,Machine Learning,Statistics',
        'interests': 'Data,Technology,Analytics',
        'degree': 'Engineering',
        'preferred_field': 'Technology'
    }

    recs = get_recommendations(test_user, df)

    print("=" * 50)
    print("TOP CAREER RECOMMENDATIONS")
    print("=" * 50)

    for i, rec in enumerate(recs, 1):
        print(f"\n{i}. {rec['Career']}")
        print(f"   Domain: {rec['Domain']}")
        print(f"   Match: {rec['Match Score']}%")
        print(f"   Skills: {rec['Matched Skills']}")