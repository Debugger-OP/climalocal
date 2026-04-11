import streamlit as st
import plotly.graph_objects as go
from data_collection import load_climate_data, CITIES
from ml_models import get_city_forecast, extract_forecast_stats, get_current_stats, predict_risk, build_risk_classifier
from carbon_profiler import calculate_carbon_footprint, get_benchmark, get_footprint_rating
import pandas as pd
from llm_engine import generate_climate_narrative
import os

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="ClimaLocal",
    page_icon="🌍",
    layout="wide"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .main-title { font-size: 3rem; font-weight: bold; color: #1A5276; text-align: center; }
    .subtitle   { font-size: 1.2rem; color: #2E8B57; text-align: center; margin-bottom: 2rem; }
    .section-header { font-size: 1.5rem; font-weight: bold; color: #1A5276; margin-top: 1rem; }
    .letter-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        color: #e0e0e0;
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #2E8B57;
        font-style: italic;
        font-size: 1.05rem;
        line-height: 1.8;
        margin: 1rem 0;
    }
    .risk-high   { background-color: #FADBD8; color: #1a1a1a; padding: 1rem; border-radius: 8px; border-left: 5px solid #E74C3C; }
    .risk-medium { background-color: #FDEBD0; color: #1a1a1a; padding: 1rem; border-radius: 8px; border-left: 5px solid #F39C12; }
    .risk-low    { background-color: #D5F5E3; color: #1a1a1a; padding: 1rem; border-radius: 8px; border-left: 5px solid #27AE60; }
    .metric-card {
        background: #EAF4FB;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border-top: 4px solid #1A5276;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown('<div class="main-title">🌍 ClimaLocal</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Personalized Hyperlocal Climate Intelligence · SDG 13: Climate Action</div>', unsafe_allow_html=True)
st.divider()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Sustainable_Development_Goal_13.png/1280px-Sustainable_Development_Goal_13.png?_=20180106212953", width=120)
    st.markdown("### ⚙️ Your Profile")

    city = st.selectbox("🏙️ Select Your City", list(CITIES.keys()))

    st.markdown("#### 🚗 Transport")
    transport_mode = st.selectbox("Mode of Transport", [
        "car_petrol", "car_diesel",
        "car_ev", "bike_ev", "scooter_ev",
        "bike_petrol",
        "auto", "bus", "bus_ev", "metro_train",
        "cycle", "work_from_home"
    ])
    daily_km = st.slider("Daily Distance (km)", 1, 100, 15)

    st.markdown("#### 🍽️ Diet")
    diet_type = st.selectbox("Diet Type", [
        "vegan", "vegetarian", "mostly_veg",
        "moderate_non_veg", "heavy_non_veg"
    ])

    st.markdown("#### ⚡ Energy")
    electricity_bill = st.slider("Monthly Electricity Bill (₹)", 100, 5000, 800)

    st.markdown("#### 🛍️ Shopping")
    shopping_habit = st.selectbox("Shopping Habit", [
        "minimal", "moderate", "frequent", "heavy"
    ])

    generate_btn = st.button("🔍 Generate My Climate Report", type="primary", use_container_width=True)

# ── Main Content ─────────────────────────────────────────────
if generate_btn:

    user_inputs = {
        "transport_mode": transport_mode,
        "daily_km": daily_km,
        "diet_type": diet_type,
        "monthly_electricity_bill": electricity_bill,
        "shopping_habit": shopping_habit,
    }

    # ── Step 1: Load & forecast climate data
    with st.spinner(f"📡 Fetching climate data for {city}..."):
        df = load_climate_data(city)

    with st.spinner("🤖 Training forecast models (this takes ~1 min)..."):
        forecasts = get_city_forecast(city)
        current_stats = get_current_stats(city)
        future_stats  = extract_forecast_stats(forecasts, target_year=2040)

    # ── Step 2: Risk classification
    build_risk_classifier()
    risk_level = predict_risk(
        future_stats["temperature"],
        future_stats["rainfall"],
        future_stats["humidity"]
    )

    # ── Step 3: Carbon footprint
    carbon_total, carbon_breakdown = calculate_carbon_footprint(user_inputs)
    rating, rating_msg = get_footprint_rating(carbon_total)
    benchmarks = get_benchmark()

    # ── Step 4: LLM Narrative
    with st.spinner("✍️ Generating your personalized climate narrative..."):
        narrative = generate_climate_narrative(
            city_name=city,
            current_stats=current_stats,
            future_stats=future_stats,
            risk_level=risk_level,
            carbon_total=carbon_total,
            carbon_breakdown=carbon_breakdown,
            user_inputs=user_inputs
        )

    # ════════════════════════════════════════════════
    # SECTION 1: City Climate Overview
    # ════════════════════════════════════════════════
    st.markdown("## 🌡️ Climate Overview")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Temperature 2040", f"{future_stats['temperature']}°C",
                  delta=f"{round(future_stats['temperature'] - current_stats['temperature'], 2)}°C vs today")
    with col2:
        st.metric("Avg Rainfall 2040", f"{future_stats['rainfall']} mm/day",
                  delta=f"{round(future_stats['rainfall'] - current_stats['rainfall'], 2)} mm vs today")
    with col3:
        st.metric("Avg Humidity 2040", f"{future_stats['humidity']}%",
                  delta=f"{round(future_stats['humidity'] - current_stats['humidity'], 2)}% vs today")

    # Risk badge
    risk_class = {"High": "risk-high", "Medium": "risk-medium", "Low": "risk-low"}.get(risk_level, "risk-low")
    risk_emoji = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}.get(risk_level, "🟢")
    st.markdown(f'<div class="{risk_class}"><b>{risk_emoji} Climate Risk Level: {risk_level}</b><br>{narrative["summary"]}</div>', unsafe_allow_html=True)

    st.divider()

    # ════════════════════════════════════════════════
    # SECTION 2: Temperature Forecast Chart
    # ════════════════════════════════════════════════
    st.markdown("## 📈 Temperature Forecast (2000–2040)")

    temp_forecast = forecasts["temperature"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=temp_forecast["ds"], y=temp_forecast["yhat"],
        name="Forecast", line=dict(color="#E74C3C", width=2)
    ))
    fig.add_trace(go.Scatter(
        x=temp_forecast["ds"], y=temp_forecast["yhat_upper"],
        fill=None, line=dict(color="rgba(231,76,60,0.2)"), showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=temp_forecast["ds"], y=temp_forecast["yhat_lower"],
        fill="tonexty", line=dict(color="rgba(231,76,60,0.2)"),
        name="Confidence Range"
    ))
    fig.add_vline(x=pd.Timestamp("2026-01-01").timestamp() * 1000,
            line_dash="dash", line_color="gray",
            annotation_text="Today")
    fig.update_layout(
        xaxis_title="Year", yaxis_title="Temperature (°C)",
        plot_bgcolor="#f9f9f9", height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ════════════════════════════════════════════════
    # SECTION 3: Carbon Footprint
    # ════════════════════════════════════════════════
    st.markdown("## 💨 Your Carbon Footprint")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"### {rating}")
        st.markdown(f"**{carbon_total} tonnes CO₂/year**")
        st.caption(rating_msg)

        # Benchmark comparison
        fig2 = go.Figure(go.Bar(
            x=["You", "India Avg", "Global Avg", "Target"],
            y=[carbon_total, benchmarks["India Average"],
                benchmarks["Global Average"], benchmarks["Sustainable Target"]],
            marker_color=["#E74C3C", "#F39C12", "#3498DB", "#27AE60"]
        ))
        fig2.update_layout(
            yaxis_title="Tonnes CO₂/year",
            plot_bgcolor="#f9f9f9", height=300
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        # Breakdown pie chart
        fig3 = go.Figure(go.Pie(
            labels=list(carbon_breakdown.keys()),
            values=list(carbon_breakdown.values()),
            hole=0.4,
            marker_colors=["#E74C3C", "#F39C12", "#3498DB", "#27AE60"]
        ))
        fig3.update_layout(height=300)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown(f"**Personal Impact:** {narrative['impact']}")

    st.divider()

    # ════════════════════════════════════════════════
    # SECTION 4: Action Plan
    # ════════════════════════════════════════════════
    st.markdown("## ✅ Your Personal Action Plan")
    for i, action in enumerate(narrative["actions"], 1):
        st.markdown(f"**{i}.** {action}")

    st.divider()

    # ════════════════════════════════════════════════
    # SECTION 5: Letter from 2040
    # ════════════════════════════════════════════════
    st.markdown("## 💌 A Letter From Your 2040 Self")
    st.markdown(f'<div class="letter-box">{narrative["letter"]}</div>', unsafe_allow_html=True)

else:
    # Landing state
    st.markdown("### 👈 Select your city and lifestyle from the sidebar, then click Generate!")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📡 **Real Climate Data**\nPulled from NASA POWER API for your exact city")
    with col2:
        st.info("🤖 **ML Forecasting**\nProphet model predicts your city's climate up to 2040")
    with col3:
        st.info("💌 **Letter from 2040**\nAI writes your personal climate future story")

# ── Footer ───────────────────────────────────────────────────
st.markdown("""
<style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #0e1117;
        padding: 0.6rem;
        text-align: center;
        color: #888;
        font-size: 0.82rem;
        border-top: 1px solid #333;
        z-index: 999;
    }
</style>
<div class="footer">
    Built with 💚 & questionable sleep schedules by <b style="color: #2E8B57;">Saurav Sharma</b> · 
    Powered by NASA data, real ML & one very real fear of Gurgaon's summers in 2040 ☀️🥵 · 
    <i>I don't bite — unless you're a bug 🐛 in my pipeline</i>
</div>
""", unsafe_allow_html=True)