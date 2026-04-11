# ── EMISSION FACTORS ─────────────────────────────────────────
# All values in kg CO2 per unit
# Sources: IPCC, MoEFCC India, GHG Protocol

EMISSION_FACTORS = {

    # Transport (kg CO2 per km)
    "transport": {
        # Petrol/Diesel
        "car_petrol":      0.21,
        "car_diesel":      0.17,
        "bike_petrol":     0.09,
        # Electric
        "car_ev":          0.05,
        "bike_ev":         0.02,
        "scooter_ev":      0.02,
        # Public
        "auto":            0.07,
        "bus":             0.03,
        "bus_ev":          0.01,
        "metro_train":     0.01,
        # Other
        "cycle":           0.0,
        "work_from_home":  0.0,
    },

    # Diet (kg CO2 per day)
    "diet": {
        "heavy_non_veg":  7.2,
        "moderate_non_veg": 5.0,
        "mostly_veg":     3.0,
        "vegetarian":     2.5,
        "vegan":          1.5,
    },

    # Electricity (kg CO2 per kWh) — India grid average
    "electricity": 0.82,

    # Shopping (kg CO2 per month estimate)
    "shopping": {
        "minimal":   10.0,
        "moderate":  30.0,
        "frequent":  60.0,
        "heavy":     100.0,
    }
}


def calculate_carbon_footprint(user_inputs):
    """
    Calculate annual carbon footprint in tonnes CO2.

    user_inputs dict keys:
    - transport_mode: str
    - daily_km: float
    - diet_type: str
    - monthly_electricity_bill: float (INR)
    - shopping_habit: str
    """

    total_kg = 0.0

    # 1. Transport
    transport_mode = user_inputs.get("transport_mode", "bus")
    daily_km = user_inputs.get("daily_km", 10)
    transport_factor = EMISSION_FACTORS["transport"].get(transport_mode, 0.05)
    transport_annual = transport_factor * daily_km * 365
    total_kg += transport_annual

    # 2. Diet
    diet_type = user_inputs.get("diet_type", "vegetarian")
    diet_factor = EMISSION_FACTORS["diet"].get(diet_type, 3.0)
    diet_annual = diet_factor * 365
    total_kg += diet_annual

    # 3. Electricity
    # Average electricity bill in India: ~Rs 7/unit
    monthly_bill = user_inputs.get("monthly_electricity_bill", 500)
    monthly_units = monthly_bill / 7.0
    electricity_annual = monthly_units * 12 * EMISSION_FACTORS["electricity"]
    total_kg += electricity_annual

    # 4. Shopping
    shopping_habit = user_inputs.get("shopping_habit", "moderate")
    shopping_factor = EMISSION_FACTORS["shopping"].get(shopping_habit, 30.0)
    shopping_annual = shopping_factor * 12
    total_kg += shopping_annual

    # Convert to tonnes
    total_tonnes = round(total_kg / 1000, 2)

    # Breakdown for display
    breakdown = {
        "Transport":   round(transport_annual / 1000, 2),
        "Diet":        round(diet_annual / 1000, 2),
        "Electricity": round(electricity_annual / 1000, 2),
        "Shopping":    round(shopping_annual / 1000, 2),
    }

    return total_tonnes, breakdown


def get_benchmark():
    """
    Return average carbon footprints for comparison (tonnes CO2/year).
    """
    return {
        "Global Average":  4.7,
        "India Average":   1.9,
        "Sustainable Target": 2.0,
    }


def get_footprint_rating(total_tonnes):
    """
    Rate the user's footprint.
    """
    if total_tonnes <= 1.5:
        return "🟢 Excellent", "Your footprint is well below the India average. Keep it up!"
    elif total_tonnes <= 2.5:
        return "🟡 Good", "Your footprint is near the India average. Small changes can make a big difference."
    elif total_tonnes <= 4.0:
        return "🟠 Moderate", "Your footprint is above the India average. Consider reducing transport or diet emissions."
    else:
        return "🔴 High", "Your footprint is significantly above average. Major lifestyle changes are recommended."


# ── Quick test ───────────────────────────────────────────────
if __name__ == "__main__":
    sample_user = {
        "transport_mode": "car_petrol",
        "daily_km": 20,
        "diet_type": "moderate_non_veg",
        "monthly_electricity_bill": 1200,
        "shopping_habit": "frequent",
    }

    total, breakdown = calculate_carbon_footprint(sample_user)
    rating, message = get_footprint_rating(total)
    benchmarks = get_benchmark()

    print(f"Total Carbon Footprint: {total} tonnes CO2/year")
    print(f"\nBreakdown:")
    for category, value in breakdown.items():
        print(f"  {category}: {value} tonnes")
    print(f"\nRating: {rating}")
    print(f"Message: {message}")
    print(f"\nBenchmarks:")
    for label, value in benchmarks.items():
        print(f"  {label}: {value} tonnes")