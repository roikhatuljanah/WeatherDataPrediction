import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Setup API
API_KEY = "14ef59ca78c8f835ed483826002c7fc0"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Daftar lengkap kota dan ibukota kabupaten di Jawa Tengah
cities = [
    "Semarang", "Surakarta", "Pekalongan", "Tegal", "Pekalongan", 
    "Salatiga", "Magelang", "Sukoharjo", "Sragen", "Karanganyar", 
    "Wonogiri", "Boyolali", "Klaten", "Purworejo", "Wonosobo", 
    "Kebumen", "Magelang", "Purwokerto", "Cilacap", "Purbalingga", 
    "Pemalang", "Tegal", "Brebes", "Pati", "Kudus", 
    "Jepara", "Demak", "Ungaran", "Kendal", "Pekalongan", 
    "Purwodadi", "Blora", "Rembang", "Cepu", "Pati"
]

# Fungsi untuk mendapatkan data cuaca
@st.cache_data
def get_weather_data(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Untuk mendapatkan suhu dalam Celsius
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

# Fungsi untuk mengambil dan menyimpan data
@st.cache_data
def fetch_all_weather_data():
    weather_data = []
    for city in cities:
        data = get_weather_data(city)
        if data["cod"] == 200:
            weather_data.append({
                "city": city,
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    return pd.DataFrame(weather_data)

# Streamlit app
st.title("Analisis Cuaca Jawa Tengah")

# Fetch data
if st.button("Ambil Data Cuaca Terbaru"):
    df = fetch_all_weather_data()
    st.success("Data cuaca berhasil diambil!")
else:
    st.warning("Klik tombol di atas untuk mengambil data cuaca terbaru.")
    st.stop()

# Tampilkan dataframe
st.subheader("Data Cuaca")
st.dataframe(df)

# Analisis Data
st.subheader("Analisis Data:")
st.write(f"Rata-rata suhu: {df['temperature'].mean():.2f}°C")
st.write(f"Kota dengan suhu tertinggi: {df.loc[df['temperature'].idxmax(), 'city']} ({df['temperature'].max():.2f}°C)")
st.write(f"Kota dengan suhu terendah: {df.loc[df['temperature'].idxmin(), 'city']} ({df['temperature'].min():.2f}°C)")
st.write(f"Kondisi cuaca paling umum: {df['description'].mode().values[0]}")

# Visualisasi Data
st.subheader("Visualisasi Data")

# Grafik Suhu
st.write("Suhu di Kota-kota Jawa Tengah")
fig, ax = plt.subplots(figsize=(15, 8))
sns.barplot(x='city', y='temperature', data=df, ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)

# Grafik Kondisi Cuaca
st.write("Distribusi Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(10, 10))
df['description'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
plt.axis('equal')
st.pyplot(fig)

# Temperature Distribution
st.write("Distribusi Temperatur")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df['temperature'], bins=10, kde=True, ax=ax)
plt.title('temperature Distribution')
plt.xlabel('temperature (°C)')
plt.ylabel('Frequency')
st.pyplot(fig)

# Tampilkan data kota dan temperatur
st.write("Data kota dan temperatur:")
st.dataframe(df[['city', 'temperature']])

# Download data
if st.button("Download Data CSV"):
    csv = df.to_csv(index=False)
    st.download_button(
        label="Klik untuk download",
        data=csv,
        file_name="weather_data_jateng.csv",
        mime="text/csv",
    )