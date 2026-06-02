"""
Machine Learning Engine for Career Classification
================================================
Trains multiple classification models and compares accuracy
Automatically selects the best performing model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import warnings

warnings.filterwarnings('ignore')


# ============================================================================
# DATA PREPARATION FUNCTIONS
# ============================================================================

def prepare_data(careers_df):
    """
    Prepares career data for ML training.
    Converts text-based skills into numerical binary features.

    Args:
        careers_df: DataFrame containing career data

    Returns:
        X: Feature matrix (skills as binary columns)
        y: Target vector (encoded domains)
        le: LabelEncoder for domains
    """
    # Create a copy to avoid modifying original
    df = careers_df.copy()

    # Convert skills string to list
    df['Skills_List'] = df['Required Skills'].apply(
        lambda x: [s.strip().lower() for s in str(x).split(',')]
    )

    # Get all unique skills across all careers
    all_skills = set()
    for skills in df['Skills_List']:
        all_skills.update(skills)

    # Create binary columns for each skill (1 if user has skill, 0 otherwise)
    for skill in all_skills:
        df[f'skill_{skill}'] = df['Skills_List'].apply(
            lambda x: 1 if skill in x else 0
        )

    # Select feature columns (all skill binary columns)
    feature_cols = [col for col in df.columns if col.startswith('skill_')]
    X = df[feature_cols].values

    # Encode Domain as target variable
    le = LabelEncoder()
    y = le.fit_transform(df['Domain'])

    return X, y, le


# ============================================================================
# MODEL TRAINING FUNCTIONS
# ============================================================================

def train_and_compare_models(careers_df):
    """
    Trains 4 different classification models and compares accuracy.

    Models trained:
    - Logistic Regression
    - Decision Tree
    - Random Forest
    - K-Nearest Neighbors

    Args:
        careers_df: DataFrame with career data

    Returns:
        results: Dictionary of model names and accuracies
        best_model_name: Name of best performing model
        best_accuracy: Accuracy of best model
    """
    print("\n" + "=" * 60)
    print("TRAINING MACHINE LEARNING MODELS")
    print("=" * 60)

    # Prepare data
    X, y, le = prepare_data(careers_df)
    print(f"\nData prepared: {X.shape[0]} samples, {X.shape[1]} features")
    print(f"Domains: {list(le.classes_)}")

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Define models to train
    models = {
        'Logistic Regression': LogisticRegression(max_iter=500, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5)
    }

    results = {}

    # Train and evaluate each model
    print("\nTraining models...")
    print("-" * 40)

    for name, model in models.items():
        # Train the model
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = accuracy

        print(f"  {name}: {accuracy:.2%}")

    # Find best model
    best_model_name = max(results, key=results.get)
    best_accuracy = results[best_model_name]

    print("\n" + "=" * 60)
    print(f"BEST MODEL: {best_model_name}")
    print(f"BEST ACCURACY: {best_accuracy:.2%}")
    print("=" * 60)

    return results, best_model_name, best_accuracy


def predict_domain(user_skills, careers_df, model_name='Random Forest'):
    """
    Predicts suitable career domain based on user skills.

    Args:
        user_skills: List of skills from user
        careers_df: DataFrame with career data
        model_name: Which model to use for prediction

    Returns:
        predicted_domain: Name of predicted career domain
    """
    # Prepare data
    X, y, le = prepare_data(careers_df)

    # Train the selected model on all data
    if model_name == 'Random Forest':
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    elif model_name == 'Decision Tree':
        model = DecisionTreeClassifier(random_state=42)
    elif model_name == 'KNN':
        model = KNeighborsClassifier(n_neighbors=5)
    else:
        model = LogisticRegression(max_iter=500, random_state=42)

    model.fit(X, y)

    # Get all skill column names
    all_skills = [col.replace('skill_', '') for col in careers_df.columns
                  if col.startswith('skill_')]

    # Create user skill vector (binary)
    user_skills_lower = [s.lower() for s in user_skills]
    user_skill_vector = [1 if skill in user_skills_lower else 0
                         for skill in all_skills]

    # Make prediction
    prediction = model.predict([user_skill_vector])
    predicted_domain = le.inverse_transform(prediction)[0]

    return predicted_domain


# ============================================================================
# MAIN FUNCTION FOR TESTING
# ============================================================================

if __name__ == "__main__":
    # Test the ML engine with sample data
    careers_df = pd.read_csv('../data/careers.csv')
    results, best_model, best_acc = train_and_compare_models(careers_df)

    print("\nTesting prediction with sample skills...")
    test_skills = ['Python', 'SQL', 'Machine Learning', 'Statistics']
    predicted = predict_domain(test_skills, careers_df, best_model)
    print(f"User skills: {test_skills}")
    print(f"Predicted domain: {predicted}")