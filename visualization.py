"""
Visualization Module
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter

sns.set_style("whitegrid")


def plot_career_scores(recommendations):
    """Plot career match scores."""
    careers = [rec['Career'] for rec in recommendations]
    scores = [rec['Match Score'] for rec in recommendations]

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(careers)))
    ax.barh(careers[::-1], scores[::-1], color=colors[::-1])
    ax.set_xlabel('Match Percentage (%)')
    ax.set_title('Career Match Scores')
    ax.set_xlim(0, 110)
    plt.tight_layout()
    return fig


def plot_model_comparison(results):
    """Plot model comparison."""
    models = list(results.keys())
    accuracies = list(results.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6']
    ax.bar(models, accuracies, color=colors)
    ax.set_ylabel('Accuracy')
    ax.set_title('ML Model Comparison')
    ax.set_ylim(0, 1.2)
    plt.tight_layout()
    return fig