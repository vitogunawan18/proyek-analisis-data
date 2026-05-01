import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

sns.set(style='dark')
st.set_page_config(page_title="E-Commerce Dashboard", page_icon="🛒", layout="wide")

# Load data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "main_data.csv")
    df = pd.read_csv(file_path)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

all_df = load_data()

st.title("🛒 E-Commerce Public Dataset Dashboard")
st.markdown("Dashboard ini menampilkan hasil analisis data E-Commerce Public Dataset dengan visualisasi interaktif.")

# Sidebar
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.header("Filter Data")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

# Question 1
st.subheader("Kategori Produk Terbaik dan Terburuk berdasarkan Jumlah Pesanan")
col1, col2 = st.columns(2)

category_counts = main_df['product_category_name_english'].value_counts().reset_index()
category_counts.columns = ['product_category', 'order_count']

top_10 = category_counts.head(10)
bottom_10 = category_counts.tail(10).sort_values(by='order_count', ascending=True)

with col1:
    st.markdown("**Top 10 Kategori Produk Terbaik**")
    fig, ax = plt.subplots(figsize=(8, 5))
    colors_main = ["#068DA9"] + ["#D3D3D3"] * 9
    sns.barplot(x="order_count", y="product_category", data=top_10, palette=colors_main, ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel('Number of Orders')
    st.pyplot(fig)

with col2:
    st.markdown("**Top 10 Kategori Produk Terburuk**")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="order_count", y="product_category", data=bottom_10, palette=colors_main, ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel('Number of Orders')
    st.pyplot(fig)

# Question 2
st.subheader("Tren Pendapatan Penjualan Bulanan (2017)")
orders_2017 = main_df[(main_df['order_purchase_timestamp'].dt.year == 2017) & (main_df['order_status'] == 'delivered')]
orders_2017['month'] = orders_2017['order_purchase_timestamp'].dt.to_period('M')
monthly_stats = orders_2017.groupby('month').agg({'price': 'sum'}).reset_index()
monthly_stats.rename(columns={'price': 'revenue'}, inplace=True)
monthly_stats['month'] = monthly_stats['month'].dt.to_timestamp()

if not monthly_stats.empty:
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(monthly_stats['month'], monthly_stats['revenue'], marker='o', linewidth=3, color="#068DA9", markersize=8)
    plt.xticks(rotation=45)
    ax.set_ylabel("Revenue (BRL)")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.fill_between(monthly_stats['month'], monthly_stats['revenue'], color="#068DA9", alpha=0.1)
    st.pyplot(fig)
else:
    st.info("Data untuk tahun 2017 tidak tersedia pada rentang waktu yang dipilih.")

st.caption("Copyright (c) Dicoding 2026")
