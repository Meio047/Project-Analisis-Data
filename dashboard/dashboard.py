import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Load datasets
@st.cache_data
def load_data():
    url_customers = "https://raw.githubusercontent.com/Meio047/Project-Analisis-Data/refs/heads/main/dashboard/customers_clean.csv"
    url_items = "https://raw.githubusercontent.com/Meio047/Project-Analisis-Data/refs/heads/main/dashboard/items_clean.csv"
    url_payments = "https://raw.githubusercontent.com/Meio047/Project-Analisis-Data/refs/heads/main/dashboard/payments_clean.csv"
    url_orders = "https://raw.githubusercontent.com/Meio047/Project-Analisis-Data/refs/heads/main/dashboard/orders_clean.csv"
    url_products = "https://raw.githubusercontent.com/Meio047/Project-Analisis-Data/refs/heads/main/dashboard/products_clean.csv"
    url_reviews = "https://raw.githubusercontent.com/Meio047/Project-Analisis-Data/refs/heads/main/dashboard/reviews_clean.csv"
    url_sellers = "https://raw.githubusercontent.com/Meio047/Project-Analisis-Data/refs/heads/main/dashboard/sellers_clean.csv"
    
    customers_df = pd.read_csv(url_customers)
    items_df = pd.read_csv(url_items)
    payments_df = pd.read_csv(url_payments)
    orders_df = pd.read_csv(url_orders)
    products_df = pd.read_csv(url_products)
    reviews_df = pd.read_csv(url_reviews)
    sellers_df = pd.read_csv(url_sellers)
    
    return customers_df, items_df, payments_df, orders_df, products_df, reviews_df, sellers_df

customers_df, items_df, payments_df, orders_df, products_df, reviews_df, sellers_df = load_data()

# Tren Penjualan
orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
orders_df['order_date'] = orders_df['order_purchase_timestamp'].dt.date
orders_df['order_week'] = orders_df['order_purchase_timestamp'].dt.to_period('W').astype(str)
orders_df['order_month'] = orders_df['order_purchase_timestamp'].dt.to_period('M').astype(str)

# Sidebar
st.sidebar.title("Menu Filter")


st.sidebar.subheader("Pilih Rentang Waktu")
# Tren harian
st.sidebar.subheader("Tren Harian")
default_start_date = pd.to_datetime(orders_df['order_date']).max().date() - pd.Timedelta(days=30)
default_end_date = pd.to_datetime(orders_df['order_date']).max().date()
start_date = st.sidebar.date_input("Pilih tanggal awal", default_start_date, min_value=orders_df['order_date'].min(), max_value=orders_df['order_date'].max())
end_date = st.sidebar.date_input("Pilih tanggal akhir", default_end_date, min_value=orders_df['order_date'].min(), max_value=orders_df['order_date'].max())
    
filtered_orders_days = orders_df[(orders_df['order_date'] >= pd.to_datetime(start_date).date()) & (orders_df['order_date'] <= pd.to_datetime(end_date).date())]

# Tren Mingguan
st.sidebar.subheader("Tren Mingguan")
ordered_weeks = sorted(orders_df['order_week'].unique())
default_start_week = ordered_weeks[-12]
default_end_week = ordered_weeks[-1]
start_week = st.sidebar.selectbox("Pilih minggu awal", ordered_weeks, index=ordered_weeks.index(default_start_week))
end_week = st.sidebar.selectbox("Pilih minggu akhir", ordered_weeks, index=ordered_weeks.index(default_end_week))

filtered_orders_week = orders_df[(orders_df['order_week'] >= start_week) & (orders_df['order_week'] <= end_week)]

# Bulanan
st.sidebar.subheader("Tren Bulanan")
ordered_months = sorted(orders_df['order_month'].unique())
default_start_month = ordered_months[-12]
default_end_month = ordered_months[-1]
start_month = st.sidebar.selectbox("Pilih bulan awal", ordered_months, index=ordered_months.index(default_start_month))
end_month = st.sidebar.selectbox("Pilih bulan akhir", ordered_months, index=ordered_months.index(default_end_month))

filtered_orders_month = orders_df[(orders_df['order_month'] >= start_month) & (orders_df['order_month'] <= end_month)]


st.title("Dashboard Analisis E-Commerce")

# Layout Grafik 2 Kolom
col1, col2 = st.columns(2)

# Distribusi Harga
with col1:
    st.subheader("Distribusi Harga Produk")
    max_price = np.percentile(items_df['price'], 99)
    filtered_prices = items_df[items_df['price'] <= max_price]['price']
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(filtered_prices, bins=30, kde=True, color='blue', ax=ax)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Heatmap Korelasi
with col2:
    st.subheader("Heatmap Korelasi Variabel Numerik")
    numerical_df = payments_df.select_dtypes(include=['number'])
    correlation_matrix = numerical_df.corr()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Boxplot Harga Produk
with col1:
    st.subheader("Boxplot Harga Produk")
    Q1 = items_df['price'].quantile(0.25)
    Q3 = items_df['price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    filtered_prices = items_df[(items_df['price'] >= lower_bound) & (items_df['price'] <= upper_bound)]['price']
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.boxplot(y=filtered_prices, color='orange', ax=ax)
    fig.tight_layout()
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)



# Distribusi Penjualan Weekday vs Weekend
with col2:
    st.subheader("Distribusi Penjualan Weekday vs Weekend")
    df = orders_df.copy()
    df['day_of_week'] = df['order_purchase_timestamp'].dt.dayofweek
    df['order_category'] = df['day_of_week'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
    sales_by_category = df['order_category'].value_counts().reset_index()
    sales_by_category.columns = ['order_category', 'order_count']
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.barplot(data=sales_by_category, x='order_category', y='order_count', ax=ax, palette='bright')
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Tren Harian
with col1:
    st.subheader("Tren Penjualan Harian")
    daily_trend = filtered_orders_days.groupby('order_date').size()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(daily_trend.index, daily_trend.values, marker='o', linestyle='-', color='blue', alpha=0.7)
    ax.set_xticklabels(daily_trend.index, rotation=45, ha='right')
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Tren Mingguan
with col2:
    st.subheader("Tren Penjualan Mingguan")
    weekly_trend = filtered_orders_week.groupby('order_week').size()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(weekly_trend.index, weekly_trend.values, marker='o', linestyle='-', color='green', alpha=0.7)
    ax.set_xticklabels(weekly_trend.index, rotation=45, ha='right')
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Tren Bulanan
with col1:
    st.subheader("Tren Penjualan Bulanan")
    monthly_trend = filtered_orders_month.groupby('order_month').size()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(monthly_trend.index, monthly_trend.values, marker='o', linestyle='-', color='red', alpha=0.7)
    ax.set_xticklabels(monthly_trend.index, rotation=45, ha='right')
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Kategori Produk Terlaris
with col2:
    st.subheader("Top 10 Kategori Produk Terlaris")
    merged_products_df = items_df.merge(products_df[['product_id', 'product_category_name']], on='product_id', how='left')
    category_sales = merged_products_df['product_category_name'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=category_sales.values, y=category_sales.index, ax=ax, palette='viridis')
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)


# Kategori Produk Terbaik berdasarkan Review
with col2:
    st.subheader("Top 10 Produk Terbaik Berdasarkan Review")
    merged_reviews_df = pd.merge(reviews_df[['order_id', 'review_score']], items_df[['order_id', 'product_id']], on='order_id', how='inner')
    merged_reviews_df = pd.merge(merged_reviews_df, products_df[['product_id', 'product_category_name']], on='product_id', how='inner')
    product_stats = merged_reviews_df.groupby(['product_id', 'product_category_name']).agg(
        review_score=('review_score', 'mean'),
        purchase_count=('product_id', 'count')
    ).reset_index()

    filtered_products = product_stats[product_stats['purchase_count'] >= 50]
    top_products = filtered_products.sort_values(by=['review_score', 'purchase_count'], ascending=[False, False])
    top_products_df = top_products.head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x=top_products_df['review_score'],
        y=top_products_df['product_category_name'],
        hue=top_products_df['product_category_name'],
        dodge=False,
        legend=False,
        palette='viridis',
        ax=ax
    )
    ax.set_title('Top 10 Kategori Produk Terbaik Berdasarkan Review', fontsize=14)
    ax.set_xlabel('Rata-rata Skor Review', fontsize=12)
    ax.set_ylabel('Kategori Produk', fontsize=12)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)


# Seller dengan Pendapatan Terbesar
with col1:
    st.subheader("Top 10 Seller dengan Pendapatan Terbesar")
    merged_sellers_df = items_df.merge(payments_df[['order_id', 'payment_value']], on='order_id', how='left')
    seller_revenue = merged_sellers_df.groupby('seller_id').agg({'price': 'sum', 'freight_value': 'sum', 'payment_value': 'sum'})
    seller_revenue['total_revenue'] = seller_revenue['payment_value']
    top_sellers = seller_revenue.sort_values(by='total_revenue', ascending=False).head(10)
    top_sellers = top_sellers.merge(sellers_df[['seller_id', 'seller_city', 'seller_state']], on='seller_id', how='left')

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_sellers['total_revenue'], y=top_sellers['seller_id'], hue=top_sellers['seller_id'], palette='viridis', legend=False, ax=ax)
    ax.set_title('Top 10 Seller dengan Pendapatan Terbesar', fontsize=14)
    ax.set_xlabel('Total Pendapatan (BRL)', fontsize=12)
    ax.set_ylabel('Seller ID', fontsize=12)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)


st.subheader("Kesimpulan")
st.markdown("""
- Metode pembayaran yang paling sering digunakan yaitu dengan kartu kredit.
- Pelanggan paling banyak ada di provinsi SP (Sao Paulo).
- Penjualan lebih tinggi pada weekend.
- Produk paling laris dapat diberikan promo khusus.
- Kategori produk dengan rating tinggi bisa diprioritaskan.
- Seller dengan pendapatan terbesar bisa diberikan apresiasi.
""")
