# 🌍 ClimaLocal

### Personalized Hyperlocal Climate Intelligence System

**SDG 13: Climate Action | ML + LLM Project**

---

> _"Global climate reports exist in abundance, but no tool connects YOUR city's real climate trajectory with YOUR personal lifestyle — and tells you what your future looks like in human language."_

---

## 🚀 Live Demo

[[[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://climalocal.streamlit.app)https://climalocal-sauravsharma.streamlit.app/]

---

## 📌 What is ClimaLocal?

ClimaLocal is an end-to-end **Machine Learning + LLM pipeline** that:

- 📡 Pulls **20+ years of real climate data** from NASA POWER API for any Indian city
- 🤖 Forecasts how **temperature, rainfall & humidity** will change by 2040 using Facebook Prophet
- 💨 Calculates your **personal carbon footprint** across transport, diet, electricity & shopping
- 🔴 Classifies your city's **climate risk level** (Low / Medium / High) using Random Forest
- ✍️ Uses **Gemini AI** to write a fully personalized climate narrative
- 💌 Generates a **"Climate Letter from 2040"** — written as if your future self is warning you

---

## 🖼️ Screenshots

| Landing Page              | Climate Forecast                   | Carbon Footprint       |
| ------------------------- | ---------------------------------- | ---------------------- |
| City & lifestyle selector | Prophet forecast chart (2000–2040) | Personal CO₂ breakdown |

---

## 🏗️ System Architecture

```
User Input (city + lifestyle)
        ↓
NASA POWER API → 20 years of climate data
        ↓
ML Pipeline:
  • Prophet      → Temperature / Rainfall / Humidity forecast
  • Ridge Regression  → Carbon footprint scoring
  • Random Forest    → Climate risk classification
        ↓
Gemini AI Narrative Engine
  • City climate summary
  • Personal impact statement
  • 5-point action plan
  • Letter from 2040
        ↓
Streamlit Web UI → Interactive Report
```

---

## 🛠️ Tech Stack

| Technology       | Purpose                              |
| ---------------- | ------------------------------------ |
| Python 3.13      | Core language                        |
| Streamlit        | Web UI                               |
| Facebook Prophet | Climate time-series forecasting      |
| Scikit-learn     | Carbon scoring + risk classification |
| Plotly           | Interactive charts                   |
| Google Gemini AI | Narrative generation                 |
| NASA POWER API   | Free historical climate data         |
| FPDF2            | PDF report generation                |

---

## ⚙️ Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOURUSERNAME/climalocal.git
cd climalocal
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key

Open `llm_engine.py` and set your key:

```python
API_KEY = os.environ.get("GEMINI_API_KEY", "your-key-here")
```

Get a free key at: [aistudio.google.com](https://aistudio.google.com)

### 5. Run the app

```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## ☁️ Deploy on Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New App
3. Select your repo → set main file as `app.py`
4. Go to **Advanced Settings → Secrets** and add:

```
GEMINI_API_KEY = "your-gemini-api-key"
```

5. Click **Deploy** 🚀

---

## 📁 Project Structure

```
climalocal/
│
├── app.py                  ← Main Streamlit web app
├── data_collection.py      ← NASA POWER API data fetching
├── ml_models.py            ← Prophet + Risk classifier
├── carbon_profiler.py      ← Carbon footprint calculator
├── llm_engine.py           ← Gemini AI narrative engine
│
├── data/                   ← Downloaded climate CSVs (auto-generated)
├── models/                 ← Saved ML models (auto-generated)
├── outputs/                ← Generated reports
│
├── requirements.txt        ← Python dependencies
└── .gitignore
```

---

## 🌆 Supported Cities

| Punjab     | Haryana   | Other                          |
| ---------- | --------- | ------------------------------ |
| Ludhiana   | Gurgaon   | Delhi                          |
| Kharar     | Faridabad | Mumbai                         |
| Amritsar   |           | Bengaluru                      |
| Jalandhar  |           | Chennai                        |
| Patiala    |           | Hyderabad                      |
| Chandigarh |           | Kolkata                        |
|            |           | Jaipur, Pune, Ahmedabad, Noida |

---

## 🎯 SDG 13 Alignment

This project directly supports **SDG 13 — Climate Action**:

- **Target 13.3** — Improves climate education at the individual level
- **Target 13.b** — Enables personal action planning based on real local data
- Makes climate change feel **personal and local**, not abstract and global

---

## 📊 ML Models Used

| Model            | Purpose              | Why                                |
| ---------------- | -------------------- | ---------------------------------- |
| Facebook Prophet | Climate forecasting  | Handles seasonality + missing data |
| Random Forest    | Risk classification  | Robust on tabular data             |
| Ridge Regression | Carbon scoring       | Interpretable + fast               |
| Gemini 2.5 Flash | Narrative generation | Converts numbers to human insight  |

---

## 🤝 Contributing

Found a bug? Want to add a city? Feel free to open an issue or pull request!

---

## 📜 License

MIT License — free to use, modify and distribute.

---

<div align="center">

Built with 💚 & questionable sleep schedules by **Saurav Sharma**

Powered by NASA data, real ML & one very real fear of Ludhiana summers in 2040 ☀️🥵

_I don't bite — unless you're a bug 🐛 in my pipeline_

</div>
