import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_KEY = "your_openweathermap_api_key"

def get_coordinates(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(url).json()
    if response and isinstance(response, list) and len(response) > 0:
        return response[0]['lat'], response[0]['lon']
    else:
        return None, None

def get_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    return requests.get(url).json()

st.title("🌤️ Real-Time Weather Forecast")

city = st.text_input("Enter city name:", "New York")

if city:
    lat, lon = get_coordinates(city)
    if lat and lon:
        weather_data = get_weather(lat, lon)

        if 'list' in weather_data:
            df = pd.DataFrame(weather_data['list'])
            df['dt_txt'] = pd.to_datetime(df['dt_txt'])
            df['temp'] = df['main'].apply(lambda x: x['temp'])

            st.subheader(f"5-Day Forecast for {city.title()}")
            fig = px.line(df, x='dt_txt', y='temp', title='Temperature (°C) Over Time')
            st.plotly_chart(fig)
        else:
            st.error("Weather forecast data not found.")
    else:
        st.error("City not found. Please enter a valid city name.")




