# ── EMISSION FACTORS ─────────────────────────────────────────
EMISSION_FACTORS = {

    # Transport (kg CO2 per km)
    "transport": {
        "car_petrol":       0.21,
        "car_diesel":       0.17,
        "car_ev":           0.05,
        "bike_petrol":      0.09,
        "bike_ev":          0.02,
        "scooter_ev":       0.02,
        "auto":             0.07,
        "bus":              0.03,
        "bus_ev":           0.01,
        "carpool_petrol":   0.10,
        "carpool_ev":       0.025,
        "shared_auto":      0.04,
        "hitchhiking":      0.02,
        "metro_train":      0.01,
        "cycle":            0.0,
        "work_from_home":   0.0,
        "walk":             0.0,
    },

    # Cooking fuel (kg CO2 per day)
    "cooking": {
        "wood":             3.8,
        "coal":             3.2,
        "lpg":              1.2,
        "png":              0.9,
        "kerosene":         2.1,
        "biogas":           0.1,
        "induction":        0.5,
        "solar_cooking":    0.0,
    },

    # Diet base (kg CO2 per day)
    "diet_base": {
        "vegan":            1.5,
        "vegetarian":       2.5,
        "mostly_veg":       3.0,
        "moderate_non_veg": 5.0,
        "heavy_non_veg":    7.2,
    },

    # Specific food items (kg CO2 per serving, additional modifier)
    "food_items": {
        # Vegan
        "dal_rice":         0.3,
        "sabzi_roti":       0.4,
        "fruits_salad":     0.2,
        "poha_upma":        0.25,
        # Vegetarian
        "paneer_dish":      0.8,
        "milk_curd_daily":  0.6,
        "cheese_butter":    1.0,
        
        # Non-veg
        "chicken_weekly":   1.2,
        "mutton_weekly":    2.5,
        "fish_weekly":      0.8,
        "egg_daily":        0.9,
    },

    # Electricity (kg CO2 per kWh) — India grid average
    "electricity": 0.82,

    # Shopping (kg CO2 per month)
    "shopping": {
        "minimal":   10.0,
        "moderate":  30.0,
        "frequent":  60.0,
        "heavy":     100.0,
    },

    # Tree carbon absorption (kg CO2 per tree per year)
    "tree_absorption": 21.0,

    # Conservation actions (kg CO2 saved per year)
    "conservation": {
        "rainwater_harvesting": 50.0,
        "solar_panels":         800.0,
        "composting":           100.0,
        "reduced_ac_use":       200.0,
        "led_lights_only":      80.0,
    }
}


def calculate_carbon_footprint(user_inputs):
    total_kg = 0.0

    # 1. Transport
    transport_mode = user_inputs.get("transport_mode", "bus")
    daily_km = user_inputs.get("daily_km", 10)
    transport_factor = EMISSION_FACTORS["transport"].get(transport_mode, 0.05)
    transport_annual = transport_factor * daily_km * 365
    total_kg += transport_annual

    # 2. Cooking
    cooking_mode = user_inputs.get("cooking_mode", "lpg")
    cooking_factor = EMISSION_FACTORS["cooking"].get(cooking_mode, 1.2)
    cooking_annual = cooking_factor * 365
    total_kg += cooking_annual

    # 3. Diet base
    diet_type = user_inputs.get("diet_type", "vegetarian")
    diet_factor = EMISSION_FACTORS["diet_base"].get(diet_type, 2.5)
    diet_annual = diet_factor * 365

    # 4. Food items modifier
    food_items = user_inputs.get("food_items", [])
    food_extra = sum(EMISSION_FACTORS["food_items"].get(item, 0) for item in food_items) * 52
    total_kg += diet_annual + food_extra

    # 5. Electricity
    monthly_bill = user_inputs.get("monthly_electricity_bill", 500)
    monthly_units = monthly_bill / 7.0
    electricity_annual = monthly_units * 12 * EMISSION_FACTORS["electricity"]
    total_kg += electricity_annual

    # 6. Shopping
    shopping_habit = user_inputs.get("shopping_habit", "moderate")
    shopping_annual = EMISSION_FACTORS["shopping"].get(shopping_habit, 30.0) * 12
    total_kg += shopping_annual

    # 7. Tree offset
    trees_planted = user_inputs.get("trees_planted", 0)
    tree_offset = trees_planted * EMISSION_FACTORS["tree_absorption"]

    # 8. Conservation offset
    conservation_actions = user_inputs.get("conservation_actions", [])
    conservation_offset = sum(EMISSION_FACTORS["conservation"].get(a, 0) for a in conservation_actions)

    total_offset = tree_offset + conservation_offset
    net_kg = max(0, total_kg - total_offset)

    breakdown = {
        "Transport":    round(transport_annual / 1000, 2),
        "Cooking":      round(cooking_annual / 1000, 2),
        "Diet & Food":  round((diet_annual + food_extra) / 1000, 2),
        "Electricity":  round(electricity_annual / 1000, 2),
        "Shopping":     round(shopping_annual / 1000, 2),
    }

    offsets = {
        "Trees Planted":    round(tree_offset / 1000, 2),
        "Conservation":     round(conservation_offset / 1000, 2),
        "Total Offset":     round(total_offset / 1000, 2),
    }

    return round(total_kg / 1000, 2), round(net_kg / 1000, 2), breakdown, offsets


def get_balance_actions(net_tonnes, trees_already_planting=0):
    """
    Tell the user exactly what they need to do to offset their footprint.
    Accounts for trees they are already planting.
    """
    trees_needed_total = net_tonnes * 1000 / EMISSION_FACTORS["tree_absorption"]

    if trees_already_planting >= trees_needed_total:
        # User is already planting enough
        trees_message = f"Keep planting {trees_already_planting} trees/year — you're already offsetting your footprint! 🎉"
        extra_trees = 0
        years_to_balance = 0
    else:
        # How many more trees per year they need
        extra_trees = round(trees_needed_total - trees_already_planting)
        if trees_already_planting > 0:
            trees_message = f"Keep planting {trees_already_planting} trees/year + plant {extra_trees} more/year to fully balance"
        else:
            trees_message = f"Plant {extra_trees} trees per year to balance your footprint"
        years_to_balance = round(trees_needed_total / max(trees_already_planting, 1)) if trees_already_planting > 0 else None

    solar_months = round((net_tonnes * 1000) / (EMISSION_FACTORS["conservation"]["solar_panels"] / 12))

    return {
        "trees_message":     trees_message,
        "trees_per_year":    trees_already_planting,
        "extra_trees":       extra_trees,
        "solar_months":      solar_months,
        "years_to_balance":  years_to_balance,
        "car_km_to_avoid":   round(net_tonnes * 1000 / EMISSION_FACTORS["transport"]["car_petrol"]),
    }


def get_benchmark():
    return {
        "Global Average":     4.7,
        "India Average":      1.9,
        "Sustainable Target": 2.0,
    }


def get_footprint_rating(net_tonnes):
    if net_tonnes <= 1.5:
        return "🟢 Excellent", "Your net footprint is well below the India average. Keep it up!"
    elif net_tonnes <= 2.5:
        return "🟡 Good", "Your footprint is near the India average. Small changes can make a big difference."
    elif net_tonnes <= 4.0:
        return "🟠 Moderate", "Your footprint is above the India average. Consider reducing transport or diet emissions."
    else:
        return "🔴 High", "Your footprint is significantly above average. Major lifestyle changes are recommended."


if __name__ == "__main__":
    sample = {
        "transport_mode": "car_petrol",
        "daily_km": 20,
        "cooking_mode": "lpg",
        "diet_type": "moderate_non_veg",
        "food_items": ["chicken_weekly", "milk_curd_daily"],
        "monthly_electricity_bill": 1200,
        "shopping_habit": "frequent",
        "trees_planted": 5,
        "conservation_actions": ["led_lights_only", "composting"],
    }

    gross, net, breakdown, offsets = calculate_carbon_footprint(sample)
    rating, msg = get_footprint_rating(net)
    balance = get_balance_actions(net)

    print(f"Gross Footprint: {gross} tonnes CO2/year")
    print(f"Net Footprint:   {net} tonnes CO2/year")
    print(f"\nBreakdown: {breakdown}")
    print(f"Offsets:   {offsets}")
    print(f"Rating:    {rating} — {msg}")
    print(f"\nTo balance your footprint:")
    print(f"  Plant {balance['trees_to_plant']} trees")
    print(f"  Or use solar panels for {balance['solar_months']} months")
    print(f"  Or avoid {balance['car_km_to_avoid']} km of car travel")