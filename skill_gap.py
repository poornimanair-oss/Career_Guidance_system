"""
Skill Gap Analysis Module
=========================
Identifies missing skills and suggests courses
to bridge the gap between current skills and career requirements
"""

import pandas as pd


# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_courses(filepath='data/courses.csv'):
    """
    Load courses dataset from CSV.

    Args:
        filepath: Path to courses.csv

    Returns:
        DataFrame with course data
    """
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return pd.DataFrame()


# ============================================================================
# SKILL GAP ANALYSIS FUNCTIONS
# ============================================================================

def analyze_gaps(recommendations, user_skills, courses_df):
    """
    Analyze skill gaps for each recommended career.

    Args:
        recommendations: List of career recommendations
        user_skills: List of user's current skills
        courses_df: DataFrame with available courses

    Returns:
        List of skill gap analysis results
    """
    skill_gaps = []

    # Create skill to course mapping (case-insensitive)
    course_map = {}
    for _, row in courses_df.iterrows():
        skill_key = str(row['Skill']).strip().lower()
        course_map[skill_key] = row['Course Name']

    # Convert user skills to set for fast lookup
    user_skills_set = set([s.lower() for s in user_skills])

    # Analyze each career
    for rec in recommendations:
        required = set([s.lower() for s in rec['Required Skills']])
        matched = set([s.lower() for s in rec['Matched Skills']])
        missing = required - matched

        # Find courses for missing skills
        suggested_courses = []
        for skill in missing:
            if skill in course_map:
                suggested_courses.append(course_map[skill])
            else:
                # Generic course suggestion
                suggested_courses.append(f"{skill.title()} Course")

        skill_gaps.append({
            'Career': rec['Career'],
            'Matched Skills': list(matched),
            'Missing Skills': list(missing),
            'Suggested Courses': suggested_courses
        })

    return skill_gaps


def get_skill_summary(skill_gaps):
    """
    Create a summary of all unique missing skills across careers.

    Args:
        skill_gaps: List of skill gap analysis results

    Returns:
        Dictionary with aggregated skill gap information
    """
    all_missing = set()
    all_courses = set()

    for gap in skill_gaps:
        all_missing.update(gap['Missing Skills'])
        all_courses.update(gap['Suggested Courses'])

    return {
        'unique_missing_skills': list(all_missing),
        'total_courses_needed': len(all_missing),
        'suggested_courses': list(all_courses)
    }


# ============================================================================
# TEST FUNCTION
# ============================================================================

if __name__ == "__main__":
    # Test with sample data
    from recommendation import load_careers, get_recommendations

    careers_df = load_careers()
    courses_df = load_courses()

    test_user = {
        'name': 'Jane',
        'skills': 'Python,Excel,SQL',
        'interests': 'Data,Analytics',
        'degree': 'Commerce',
        'preferred_field': 'Business'
    }

    recs = get_recommendations(test_user, careers_df)
    gaps = analyze_gaps(recs, test_user.get('skills', '').split(','), courses_df)

    print("=" * 50)
    print("SKILL GAP ANALYSIS")
    print("=" * 50)

    for gap in gaps:
        print(f"\n{gap['Career']}")
        print(f"  Missing: {', '.join(gap['Missing Skills'])}")
        print(f"  Courses: {', '.join(gap['Suggested Courses'])}")