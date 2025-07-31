import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ------------------- SETUP -------------------
API_KEY = "your_api_key_here"  # 🔁 Replace this with your actual API key

# Predefined cities and their coordinates
CITIES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "London": {"lat": 51.5072, "lon": -0.1276},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503}
}

# AQI Categories (OpenWeatherMap scale)
AQI_LABELS = {
    1: ("Good", "🟢"),
    2: ("Fair", "🟡"),
    3: ("Moderate", "🟠"),
    4: ("Poor", "🔴"),
    5: ("Very Poor", "🟣")
}

# ------------------- FUNCTIONS -------------------

def get_aqi_data(lat, lon):
    """Fetch air quality data for given coordinates from OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "list" not in data or len(data["list"]) == 0:
            return None, "No air quality data found for this location."
        return data["list"][0], None
    except Exception as e:
        return None, f"API request failed: {e}"

# ------------------- STREAMLIT UI -------------------

st.set_page_config(page_title="AQI Dashboard", layout="centered")
st.title("🌫️ Real-Time Air Quality Index (AQI) Dashboard")

# City selection
city = st.selectbox("Choose a City", list(CITIES.keys()))
coords = CITIES[city]

# Fetch data
with st.spinner("Fetching real-time AQI data..."):
    data, error = get_aqi_data(coords["lat"], coords["lon"])

# Handle errors
if error:
    st.error(f"❌ {error}")
    st.stop()

# Extract AQI and pollutant data
aqi = data["main"]["aqi"]
components = data["components"]
aqi_label, emoji = AQI_LABELS.get(aqi, ("Unknown", "❓"))

# ------------------- DISPLAY RESULTS -------------------

st.metric(label="Air Quality Index", value=f"{aqi} - {aqi_label} {emoji}")

# Pollutant bar chart
st.subheader("🔬 Pollutant Concentrations (μg/m³)")
df = pd.DataFrame(list(components.items()), columns=["Pollutant", "Concentration"])
fig = px.bar(df, x="Pollutant", y="Concentration", color="Pollutant",
             title=f"Pollutant Levels in {city}", height=400)
st.plotly_chart(fig, use_container_width=True)

# Health advisory
st.subheader("📋 Health Advisory")
if aqi == 1:
    st.success("Air quality is good. It's safe to go outside.")
elif aqi == 2:
    st.info("Air quality is fair. Sensitive individuals should be aware.")
elif aqi == 3:
    st.warning("Moderate air quality. Consider reducing prolonged outdoor activity.")
elif aqi == 4:
    st.error("Poor air quality. Limit outdoor exposure and wear a mask.")
elif aqi == 5:
    st.error("Very poor air quality. Stay indoors and use air purifiers if possible.")
else:
    st.info("No advisory available.")

# Optional: Show raw data for debugging
with st.expander("🔍 Show Raw API Response (for debugging)"):
    st.json(data)


