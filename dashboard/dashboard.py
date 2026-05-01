import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
import matplotlib.ticker as ticker

# Remove sns.set(style='dark') to match notebook's default white style
st.set_page_config(page_title="E-Commerce Dashboard", page_icon="🛒", layout="wide")

# Load data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    main_path = os.path.join(base_dir, "main_data.csv")
    cust_path = os.path.join(base_dir, "customers_dataset.csv")
    
    df = pd.read_csv(main_path)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    
    # Load customers for RFM
    cust_df = pd.read_csv(cust_path)
    return df, cust_df

all_df, customers_df = load_data()

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

sum_order_items_df = main_df.groupby("product_category_name_english").order_id.nunique().reset_index().rename(columns={"order_id": "order_count"}).sort_values(by="order_count", ascending=False)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="order_count", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Product", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)

sns.barplot(x="order_count", y="product_category_name_english", data=sum_order_items_df.sort_values(by="order_count", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

plt.suptitle("Best and Worst Performing Product by Number of Sales", fontsize=20)
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
    ax.set_title("Total Monthly Sales Revenue in 2017 (BRL)", loc="center", fontsize=22, fontweight='bold')
    ax.tick_params(axis='x', labelsize=12, rotation=45)
    ax.tick_params(axis='y', labelsize=12)
    ax.set_ylabel("Revenue (BRL)", fontsize=15)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.fill_between(monthly_stats['month'], monthly_stats['revenue'], color="#068DA9", alpha=0.1)
    st.pyplot(fig)
else:
    st.info("Data untuk tahun 2017 tidak tersedia pada rentang waktu yang dipilih.")

# RFM Analysis
st.subheader("Best Customers Based on RFM Parameters")

rfm_df = main_df[main_df['order_status'] == 'delivered'].copy()
rfm_df = pd.merge(rfm_df, customers_df, on="customer_id")
recent_date = all_df['order_purchase_timestamp'].max()

rfm = rfm_df.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (recent_date - x.max()).days + 1,
    'order_id': 'nunique',
    'price': 'sum'
}).reset_index()

rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
rfm['short_id'] = rfm['customer_id'].str[:8]

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(24, 6))
colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# By Recency
sns.barplot(y="recency", x="short_id", data=rfm.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=12)
ax[0].set_xlabel('')
ax[0].set_ylabel('')

# By Frequency
sns.barplot(y="frequency", x="short_id", data=rfm.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=12)
ax[1].set_xlabel('')
ax[1].set_ylabel('')

# By Monetary
sns.barplot(y="monetary", x="short_id", data=rfm.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=12)
ax[2].set_xlabel('')
ax[2].set_ylabel('')
ax[2].yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

for i in range(3):
    ax[i].spines['top'].set_visible(False)
    ax[i].spines['right'].set_visible(False)

plt.suptitle("Best Customers Based on RFM Parameters", fontsize=25, fontweight='bold', y=1.05)
plt.tight_layout()
st.pyplot(fig)

st.caption("Copyright (c) Dicoding 2026")
