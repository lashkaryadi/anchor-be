"""
Flight Risk Prediction Engine

Uses a gradient-boosted model trained on employee features to predict
flight risk. Features include compensation gap, tenure, engagement trend,
manager relationship score, promotion recency, and behavioral signals.
"""

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "risk_model.joblib")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "risk_scaler.joblib")


def _generate_training_data(n_samples: int = 500):
    """Generate synthetic training data mirroring real HR patterns."""
    rng = np.random.RandomState(42)

    comp_gap = rng.uniform(-0.15, 0.25, n_samples)  # salary gap vs market (negative = above)
    tenure_years = rng.uniform(0.5, 10, n_samples)
    engagement_slope = rng.uniform(-5, 2, n_samples)  # negative = declining
    manager_score = rng.uniform(3, 10, n_samples)
    months_since_promo = rng.uniform(1, 36, n_samples)
    behavioral_signals = rng.randint(0, 5, n_samples)  # count of concerning behaviors

    # Build target: flight risk probability
    risk_signal = (
        comp_gap * 2.5
        + (1.0 / (tenure_years + 0.5)) * 0.8
        - engagement_slope * 0.15
        - (manager_score - 5) * 0.12
        + (months_since_promo / 36) * 0.6
        + behavioral_signals * 0.18
    )
    noise = rng.normal(0, 0.15, n_samples)
    prob = 1 / (1 + np.exp(-(risk_signal + noise)))
    labels = (prob > 0.5).astype(int)

    X = np.column_stack([
        comp_gap, tenure_years, engagement_slope,
        manager_score, months_since_promo, behavioral_signals,
    ])
    return X, labels


def train_model():
    """Train and persist the risk prediction model."""
    X, y = _generate_training_data()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = GradientBoostingClassifier(
        n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42
    )
    model.fit(X_scaled, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    return model, scaler


def _load_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        return joblib.load(MODEL_PATH), joblib.load(SCALER_PATH)
    return train_model()


def predict_risk_score(
    comp_gap: float,
    tenure_years: float,
    engagement_slope: float,
    manager_score: float,
    months_since_promo: float,
    behavioral_signal_count: int,
) -> dict:
    """
    Predict flight risk for a single employee.

    Returns:
        dict with risk_score (0-100), risk_level, confidence, contributing_factors
    """
    model, scaler = _load_model()

    features = np.array([[
        comp_gap, tenure_years, engagement_slope,
        manager_score, months_since_promo, behavioral_signal_count,
    ]])
    features_scaled = scaler.transform(features)

    prob = model.predict_proba(features_scaled)[0][1]
    risk_score = round(prob * 100, 1)

    if risk_score >= 75:
        risk_level = "critical"
    elif risk_score >= 55:
        risk_level = "high"
    elif risk_score >= 35:
        risk_level = "medium"
    else:
        risk_level = "low"

    # Feature importance for this prediction
    feature_names = [
        "Compensation gap", "Tenure", "Engagement trend",
        "Manager relationship", "Promotion recency", "Behavioral signals",
    ]
    importances = model.feature_importances_
    factor_list = sorted(
        zip(feature_names, importances),
        key=lambda x: x[1],
        reverse=True,
    )

    confidence = min(95, max(60, int(70 + abs(prob - 0.5) * 50)))

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "confidence": confidence,
        "top_factors": [{"name": n, "weight": round(w * 100, 1)} for n, w in factor_list[:4]],
    }
