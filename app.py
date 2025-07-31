import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ----------- CONFIGURATION -------------
API_KEY = "your_api_key_here"  # 🔁 Replace with your actual OpenWeatherMap API key
DEFAULT_CITIES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "London": {"lat": 51.5072, "lon": -0.1276},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503}
}

AQI_LABELS = {
    1: ("Good", "🟢"),
    2: ("Fair", "🟡"),
    3: ("Moderate", "🟠"),
    4: ("Poor", "🔴"),
    5: ("Very Poor", "🟣")
}

# ----------- FUNCTION TO FETCH AQI -------------
def get_aqi_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "list" not in data or len(data["list"]) == 0:
        st.error("⚠️ No air quality data available. Check API key or coordinates.")
        st.stop()

    return data["list"][0]

# ----------- STREAMLIT APP -------------
st.set_page_config(page_title="Air Quality Dashboard", layout="centered")
st.title("🌫️ Real-Time Air Quality Index (AQI) Dashboard")

city = st.selectbox("Choose a city", list(DEFAULT_CITIES.keys()))
coords = DEFAULT_CITIES[city]

with st.spinner("Fetching data..."):
    aqi_data = get_aqi_data(coords["lat"], coords["lon"])

aqi = aqi_data["main"]["aqi"]
aqi_label, emoji = AQI_LABELS.get(aqi, ("Unknown", "❓"))

st.metric(label="Air Quality Index (AQI)", value=f"{aqi} - {aqi_label} {emoji}")

# ----------- POLLUTANT CHART -------------
st.subheader("🔬 Pollutant Concentrations (μg/m³)")
components = aqi_data["components"]
df = pd.DataFrame(list(components.items()), columns=["Pollutant", "Concentration"])

fig = px.bar(df, x="Pollutant", y="Concentration", color="Pollutant",
             title=f"Pollutants in the Air - {city}", height=400)
st.plotly_chart(fig, use_container_width=True)

# ----------- HEALTH ADVICE -------------
st.subheader("📋 Health Advisory")

if aqi == 1:
    st.success("Air quality is good. Enjoy your outdoor activities!")
elif aqi == 2:
    st.info("Air quality is fair. Sensitive individuals should avoid heavy exertion.")
elif aqi == 3:
    st.warning("Air quality is moderate. Consider reducing outdoor exposure.")
elif aqi == 4:
    st.error("Air quality is poor. Avoid prolonged outdoor activities.")
elif aqi == 5:
    st.error("Air quality is very poor. Stay indoors and consider using an air purifier.")
else:
    st.info("No advisory available.")

# ----------- DEBUG (Optional) -------------
# st.write("Full API Response:", aqi_data)

