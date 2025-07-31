import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ✅ Replace this with your own working OpenWeatherMap API key
API_KEY = "your_actual_api_key_here"  # ← paste your real API key here

# ✅ Known working coordinates from OpenWeatherMap documentation & tested cities
CITIES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "Tokyo": {"lat": 35.6895, "lon": 139.6917},
    "Los Angeles": {"lat": 34.0522, "lon": -118.2437}
}

AQI_LABELS = {
    1: ("Good", "🟢"),
    2: ("Fair", "🟡"),
    3: ("Moderate", "🟠"),
    4: ("Poor", "🔴"),
    5: ("Very Poor", "🟣")
}

def get_aqi_data(lat, lon):
    """Fetch real-time air quality data using OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }

    try:
        res = requests.get(url, params=params)
        if res.status_code != 200:
            return None, f"API Error: {res.status_code} - {res.json().get('message', 'Unknown error')}"
        data = res.json()
        if "list" not in data or len(data["list"]) == 0:
            return None, "No air quality data found for this location."
        return data["list"][0], None
    except Exception as e:
        return None, f"Request failed: {e}"

# ---------- Streamlit UI ----------
st.set_page_config(page_title="AQI Dashboard", layout="centered")
st.title("🌫️ Real-Time Air Quality Index (AQI) Dashboard")

city = st.selectbox("Choose a City", list(CITIES.keys()))
coords = CITIES[city]

with st.spinner(f"Fetching AQI data for {city}..."):
    aqi_data, error = get_aqi_data(coords["lat"], coords["lon"])

# ---------- Error Handling ----------
if error:
    st.error(f"❌ {error}")
    st.stop()

# ---------- Display AQI ----------
aqi = aqi_data["main"]["aqi"]
components = aqi_data["components"]
aqi_label, emoji = AQI_LABELS.get(aqi, ("Unknown", "❓"))

st.metric("Air Quality Index", f"{aqi} - {aqi_label} {emoji}")

# ---------- Pollutant Breakdown ----------
st.subheader("🔬 Pollutant Concentrations (μg/m³)")
df = pd.DataFrame(components.items(), columns=["Pollutant", "Concentration"])
fig = px.bar(df, x="Pollutant", y="Concentration", color="Pollutant", height=400)
st.plotly_chart(fig, use_container_width=True)

# ---------- Health Advisory ----------
st.subheader("📋 Health Advisory")
if aqi == 1:
    st.success("Excellent air quality. It's safe to enjoy outdoor activities.")
elif aqi == 2:
    st.info("Fair air quality. Safe for most people.")
elif aqi == 3:
    st.warning("Moderate air quality. Sensitive individuals should limit outdoor exposure.")
elif aqi == 4:
    st.error("Poor air quality. Reduce prolonged outdoor activity.")
elif aqi == 5:
    st.error("Very poor air quality. Avoid going outside and use air purifiers.")

# ---------- Optional Debug ----------
with st.expander("🔍 Show Raw API Response"):
    st.json(aqi_data)



