import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
dingling_df = pd.read_csv("dingling_clean.csv")

# Membuat dataframe yang hanya berisi data suhu udara dan parameter polutan udara
temp_polutan = {
    "TEMP": dingling_df["TEMP"],
    "PM2.5": dingling_df["PM2.5"],
    "PM10": dingling_df["PM10"],
    "SO2": dingling_df["SO2"],
    "NO2": dingling_df["NO2"],
    "CO": dingling_df["CO"],
    "O3": dingling_df["O3"]
}
data_df = pd.DataFrame(temp_polutan)

# Menghitung korelasi antara suhu udara dan parameter polutan udara
correlation_temp = data_df.corr()

# Menjumlahkan nilai polutan dari "PM2.5", "PM10", "SO2", "NO2", "CO", dan "O3"
dingling_df['Total_Pollutants'] = dingling_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].sum(axis=1)

# Menghitung rata-rata total polutan untuk setiap bulan dalam setiap tahun
monthly_averages = dingling_df.groupby(['year', 'month'])['Total_Pollutants'].mean()

# Menentukan bulan dengan rata-rata tertinggi untuk total polutan dalam setiap tahun
max_months = monthly_averages.groupby('year').idxmax()
max_months = max_months.rename('month')

# Fungsi untuk menampilkan data
def tampilkan_data():
    # Menampilkan data utama
    st.subheader('Cleaned Data')
    st.write(dingling_df)

    # Display correlation between air temperature and air pollutant parameters
    st.subheader('Correlation between Air Temperature and Air Pollutants')
    st.write(correlation_temp["TEMP"])

    # Display monthly average total pollutants for each year
    st.subheader('Monthly Average Total Pollutants')
    st.write(monthly_averages)

    # Display month with highest average total pollutants for each year
    st.subheader('Month with Highest Average Total Pollutants')
    st.write(max_months)

# Fungsi untuk menampilkan statistik sederhana
def tampilkan_visualisasi():  
    st.set_option('deprecation.showPyplotGlobalUse', False)  
    
    # Visualisasi Pertanyaan 1: Korelasi antara suhu dan parameter kualitas udara
    st.header('Visualisasi Pertanyaan 1: Korelasi antara Suhu dan Parameter Kualitas Udara')
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_temp, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Heatmap Korelasi antara Suhu dan Parameter Kualitas Udara')
    plt.xlabel('Parameter Kualitas Udara')
    plt.ylabel('Parameter Kualitas Udara')
    st.pyplot()

    # Visualisasi Pertanyaan 2: Rata-rata total polutan per bulan
    st.header('Visualisasi Pertanyaan 2: Rata-Rata Total Polutan per Bulan')
    plt.figure(figsize=(12, 6))
    monthly_averages.plot(marker='o', color='b', linestyle='-')
    plt.title('Rata-Rata Total Polutan per Bulan')
    plt.xlabel('Tanggal')
    plt.ylabel('Rata-Rata Total Polutan')
    plt.grid(True)
    plt.xticks(range(len(monthly_averages)), [f"{year}-{month:02d}" for year, month in monthly_averages.index], rotation=90)
    plt.tight_layout()
    st.pyplot()

# Fungsi utama
def main():
    st.title('Dingling Air Quality Dashboard')

    menu = ['Tampilkan Data', 'Tampilkan Visualisasi']
    pilihan = st.sidebar.selectbox('Pilihan Menu', menu)

    if pilihan == 'Tampilkan Data':
        tampilkan_data()
    elif pilihan == 'Tampilkan Visualisasi':
        tampilkan_visualisasi()

if __name__ == '__main__':
    main()