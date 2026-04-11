import requests
import pandas as pd
import os

# Indian cities with their coordinates
CITIES = {
    "Ludhiana":   {"lat": 30.9010, "lon": 75.8573},
    "Delhi":      {"lat": 28.6139, "lon": 77.2090},
    "Mumbai":     {"lat": 19.0760, "lon": 72.8777},
    "Bengaluru":  {"lat": 12.9716, "lon": 77.5946},
    "Chennai":    {"lat": 13.0827, "lon": 80.2707},
    "Hyderabad":  {"lat": 17.3850, "lon": 78.4867},
    "Kolkata":    {"lat": 22.5726, "lon": 88.3639},
    "Jaipur":     {"lat": 26.9124, "lon": 75.7873},
    "Ahmedabad":  {"lat": 23.0225, "lon": 72.5714},
    "Pune":       {"lat": 18.5204, "lon": 73.8567},
    "Kharar":     {"lat": 30.7460, "lon": 76.6456},
    "Gurgaon":    {"lat": 28.4595, "lon": 77.0266},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794},
    "Amritsar":   {"lat": 31.6340, "lon": 74.8723},
    "Jalandhar":  {"lat": 31.3260, "lon": 75.5762},
    "Patiala":    {"lat": 30.3398, "lon": 76.3869},
    "Faridabad":  {"lat": 28.4089, "lon": 77.3178},
    "Noida":      {"lat": 28.5355, "lon": 77.3910},
}


def fetch_climate_data(city_name, start_year=2000, end_year=2023):
    """
    Fetch historical climate data from NASA POWER API for a given city.
    Returns a DataFrame with temperature, rainfall, and humidity.
    """

    if city_name not in CITIES:
        print(f"City '{city_name}' not found.")
        return None

    lat = CITIES[city_name]["lat"]
    lon = CITIES[city_name]["lon"]

    print(f"Fetching climate data for {city_name} ({start_year}–{end_year})...")

    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
    params = {
        "parameters": "T2M,PRECTOTCORR,RH2M",  # Temperature, Rainfall, Humidity
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": start_year,
        "end": end_year,
        "format": "JSON"
    }

    response = requests.get(url, params=params, timeout=60)

    if response.status_code != 200:
        print(f"API Error: {response.status_code}")
        return None

    raw = response.json()
    properties = raw["properties"]["parameter"]

    temp_data   = properties["T2M"]        # Temperature (°C)
    rain_data   = properties["PRECTOTCORR"] # Rainfall (mm/day)
    humid_data  = properties["RH2M"]        # Humidity (%)

    rows = []
    for key in temp_data:
        # key format: YYYYMM
        year  = int(key[:4])
        month = int(key[4:])
        if month == 13:   # NASA uses 13 as annual average — skip
            continue
        rows.append({
            "date":        pd.Timestamp(year=year, month=month, day=1),
            "temperature": temp_data[key],
            "rainfall":    rain_data[key],
            "humidity":    humid_data[key],
            "city":        city_name
        })

    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)

    # Save to CSV
    os.makedirs("data", exist_ok=True)
    filepath = f"data/{city_name.lower()}_climate.csv"
    df.to_csv(filepath, index=False)
    print(f"Saved: {filepath}  ({len(df)} records)")

    return df


def load_climate_data(city_name):
    """
    Load saved climate data from CSV.
    If not found, fetch it from the API.
    """
    filepath = f"data/{city_name.lower()}_climate.csv"

    if os.path.exists(filepath):
        df = pd.read_csv(filepath, parse_dates=["date"])
        print(f"Loaded existing data for {city_name} ({len(df)} records)")
        return df
    else:
        return fetch_climate_data(city_name)


# ── Quick test ──────────────────────────────────────────────
if __name__ == "__main__":
    df = fetch_climate_data("Ludhiana")
    if df is not None:
        print(df.head(10))
        print(f"\nTotal records: {len(df)}")
        print(f"Date range: {df['date'].min()} → {df['date'].max()}")