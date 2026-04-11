import pandas as pd
import numpy as np
import os
import pickle
from prophet import Prophet
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ── 1. CLIMATE FORECASTING WITH PROPHET ─────────────────────

def train_forecast_model(df, target_column):
    """
    Train a Prophet model on historical climate data.
    target_column: 'temperature', 'rainfall', or 'humidity'
    """
    # Prophet needs columns named 'ds' and 'y'
    prophet_df = df[["date", target_column]].rename(
        columns={"date": "ds", target_column: "y"}
    )

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.05
    )
    model.fit(prophet_df)
    return model


def forecast_future(model, periods=204):
    """
    Forecast future values.
    periods=204 means 17 years into the future (up to ~2040)
    """
    future = model.make_future_dataframe(periods=periods, freq="MS")
    forecast = model.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]


def get_city_forecast(city_name):
    """
    Full pipeline: load data → train models → return forecasts
    for temperature, rainfall, and humidity.
    """
    from data_collection import load_climate_data

    df = load_climate_data(city_name)
    if df is None:
        return None

    print(f"Training forecast models for {city_name}...")

    forecasts = {}
    for col in ["temperature", "rainfall", "humidity"]:
        print(f"  → Training {col} model...")
        model = train_forecast_model(df, col)
        forecast = forecast_future(model)
        forecasts[col] = forecast

    print("Done!")
    return forecasts


# ── 2. EXTRACT KEY STATS FROM FORECAST ──────────────────────

def extract_forecast_stats(forecasts, target_year=2040):
    """
    From forecast DataFrames, extract the predicted average
    values for a target year.
    """
    stats = {}
    for col, forecast_df in forecasts.items():
        future_data = forecast_df[
            forecast_df["ds"].dt.year == target_year
        ]
        if not future_data.empty:
            stats[col] = round(future_data["yhat"].mean(), 2)
        else:
            stats[col] = None
    return stats


def get_current_stats(city_name):
    """
    Get average climate stats from the most recent 3 years of data.
    """
    from data_collection import load_climate_data

    df = load_climate_data(city_name)
    recent = df[df["date"].dt.year >= 2023]
    return {
        "temperature": round(recent["temperature"].mean(), 2),
        "rainfall":    round(recent["rainfall"].mean(), 2),
        "humidity":    round(recent["humidity"].mean(), 2),
    }


# ── 3. RISK CLASSIFIER ───────────────────────────────────────

def build_risk_classifier():
    """
    Build and train a Random Forest classifier that predicts
    city climate risk level: Low / Medium / High
    Based on: avg temperature, rainfall variability, humidity
    """

    # Training data — manually labeled based on climate patterns
    training_data = [
        # temp,  rainfall, humidity, risk
        [22.0,   3.5,      65.0,     "Low"],
        [24.0,   2.8,      60.0,     "Low"],
        [26.0,   2.0,      55.0,     "Medium"],
        [28.0,   1.5,      50.0,     "Medium"],
        [30.0,   1.0,      45.0,     "Medium"],
        [32.0,   0.8,      40.0,     "High"],
        [34.0,   0.5,      35.0,     "High"],
        [36.0,   0.3,      30.0,     "High"],
        [20.0,   4.0,      70.0,     "Low"],
        [38.0,   0.2,      28.0,     "High"],
        [29.0,   1.2,      48.0,     "Medium"],
        [25.0,   2.5,      58.0,     "Low"],
        [33.0,   0.6,      38.0,     "High"],
        [27.0,   1.8,      52.0,     "Medium"],
        [21.0,   3.8,      68.0,     "Low"],
    ]

    df_train = pd.DataFrame(training_data,
        columns=["temperature", "rainfall", "humidity", "risk"])

    le = LabelEncoder()
    df_train["risk_encoded"] = le.fit_transform(df_train["risk"])

    X = df_train[["temperature", "rainfall", "humidity"]]
    y = df_train["risk_encoded"]

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)

    # Save model and encoder
    os.makedirs("models", exist_ok=True)
    with open("models/risk_classifier.pkl", "wb") as f:
        pickle.dump((clf, le), f)

    return clf, le


def predict_risk(temperature, rainfall, humidity):
    """
    Predict climate risk level for given climate stats.
    """
    model_path = "models/risk_classifier.pkl"

    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            clf, le = pickle.load(f)
    else:
        clf, le = build_risk_classifier()

    X = pd.DataFrame([[temperature, rainfall, humidity]],
                     columns=["temperature", "rainfall", "humidity"])
    prediction = clf.predict(X)
    return le.inverse_transform(prediction)[0]


# ── Quick test ───────────────────────────────────────────────
if __name__ == "__main__":
    # Test risk classifier
    print("Building risk classifier...")
    build_risk_classifier()
    risk = predict_risk(temperature=35.0, rainfall=0.5, humidity=32.0)
    print(f"Risk for hot dry conditions: {risk}")

    risk2 = predict_risk(temperature=24.0, rainfall=3.0, humidity=65.0)
    print(f"Risk for mild conditions: {risk2}")

    # Test forecast (takes 1-2 mins)
    print("\nRunning forecast for Ludhiana...")
    forecasts = get_city_forecast("Ludhiana")
    stats_2040 = extract_forecast_stats(forecasts, target_year=2040)
    print(f"\nPredicted averages for Ludhiana in 2040:")
    for k, v in stats_2040.items():
        print(f"  {k}: {v}")