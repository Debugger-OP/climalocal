from google import genai
import json
import re
import os   

# ── Paste your Gemini API key here ──────────────────────────
API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)


def generate_climate_narrative(
    city_name,
    current_stats,
    future_stats,
    risk_level,
    carbon_total,
    carbon_breakdown,
    user_inputs
):
    prompt = f"""
You are a climate intelligence assistant. Based on real ML model outputs,
generate a personalized climate report for a citizen.

--- CITY DATA ---
City: {city_name}

Current climate (2023-2026 average):
- Average Temperature: {current_stats['temperature']}°C
- Average Rainfall: {current_stats['rainfall']} mm/day
- Average Humidity: {current_stats['humidity']}%

Predicted climate in 2040 (ML forecast):
- Average Temperature: {future_stats['temperature']}°C
- Average Rainfall: {future_stats['rainfall']} mm/day
- Average Humidity: {future_stats['humidity']}%

Climate Risk Level: {risk_level}

--- PERSONAL CARBON FOOTPRINT ---
Total: {carbon_total} tonnes CO2/year
Breakdown:
- Transport: {carbon_breakdown['Transport']} tonnes
- Diet & Food: {carbon_breakdown['Diet & Food']} tonnes
- Electricity: {carbon_breakdown['Electricity']} tonnes
- Shopping: {carbon_breakdown['Shopping']} tonnes

User lifestyle:
- Transport: {user_inputs.get('transport_mode', 'unknown')} ({user_inputs.get('daily_km', 0)} km/day)
- Diet: {user_inputs.get('diet_type', 'unknown')}
- Monthly electricity bill: Rs {user_inputs.get('monthly_electricity_bill', 0)}
- Shopping habit: {user_inputs.get('shopping_habit', 'unknown')}

--- YOUR TASK ---
Generate a JSON response with exactly these 4 keys:

1. "summary": 3 sentences describing how {city_name}'s climate is changing
   and what residents will experience by 2040. Be specific and factual.

2. "impact": 3 sentences connecting the user's personal carbon footprint
   to local climate impact. Make it feel personal and real.

3. "actions": A list of exactly 5 specific actionable recommendations
   for this user ranked by impact. Each should be one sentence.

4. "letter": A Climate Letter from 2040 written in first person as if
   the user is living in {city_name} in 2040 and writing to their 2026 self.
   4-5 sentences. Emotional, vivid, and specific to {city_name}'s climate.
   Make it powerful enough to motivate real behavior change.

Return ONLY valid JSON. No extra text, no markdown, no code blocks.
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip()

    # Clean markdown if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    # Fix common JSON issues from LLM output
    raw = re.sub(r',\s*}', '}', raw)   # trailing comma in object
    raw = re.sub(r',\s*]', ']', raw)   # trailing comma in array

    result = json.loads(raw)
    return result


# ── Quick test ───────────────────────────────────────────────
if __name__ == "__main__":
    current = {"temperature": 26.5, "rainfall": 1.8,  "humidity": 42.0}
    future  = {"temperature": 22.34, "rainfall": 4.05, "humidity": 74.01}

    user_inputs = {
        "transport_mode": "car_petrol",
        "daily_km": 20,
        "diet_type": "moderate_non_veg",
        "monthly_electricity_bill": 1200,
        "shopping_habit": "frequent",
    }

    carbon_total = 5.76
    carbon_breakdown = {
        "Transport": 1.53,
        "Diet": 1.82,
        "Electricity": 1.69,
        "Shopping": 0.72
    }

    print("Generating climate narrative...")
    result = generate_climate_narrative(
        city_name="Ludhiana",
        current_stats=current,
        future_stats=future,
        risk_level="High",
        carbon_total=carbon_total,
        carbon_breakdown=carbon_breakdown,
        user_inputs=user_inputs
    )

    print("\n── CITY SUMMARY ──")
    print(result["summary"])
    print("\n── PERSONAL IMPACT ──")
    print(result["impact"])
    print("\n── ACTION PLAN ──")
    for i, action in enumerate(result["actions"], 1):
        print(f"{i}. {action}")
    print("\n── LETTER FROM 2040 ──")
    print(result["letter"])
