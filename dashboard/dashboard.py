import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



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

# Sidebar

st.sidebar.title("Dashboard E-Commerce")
kategori = ["Distribusi Harga Produk", "Heatmap Korelasi", "Distribusi Metode Pembayaran", "Distribusi Pelanggan per Negara Bagian", "Boxplot Harga Produk", "Tren Penjualan", "Distribusi Penjualan Weekday vs Weekend", "Kategori Produk Terlaris", "Produk Terbaik Berdasarkan Review", "Seller dengan Pendapatan Terbesar"]
selected_sections = st.sidebar.multiselect("Pilih Analisis", kategori, default=kategori)



st.title("Dashboard Analisis E-Commerce")

# Distribusi Harga Item
if "Distribusi Harga Produk" in selected_sections:
    st.subheader("Distribusi Harga Produk")
    max_price = np.percentile(items_df['price'], 99)
    filtered_prices = items_df[items_df['price'] <= max_price]['price']
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(filtered_prices, bins=30, kde=True, color='blue', ax=ax)
    ax.set_title('Distribusi Harga Item')
    st.pyplot(fig)

# Heatmap Korelasi
if "Heatmap Korelasi" in selected_sections:
    st.subheader("Heatmap Korelasi Variabel Numerik")
    numerical_df = payments_df.select_dtypes(include=['number'])
    correlation_matrix = numerical_df.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
    st.pyplot(fig)

# Boxplot Harga Produk
if "Boxplot Harga Produk" in selected_sections:
    st.subheader("Boxplot Distribusi Harga Produk (Tanpa Outlier)")
    Q1 = items_df['price'].quantile(0.25)
    Q3 = items_df['price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    filtered_prices = items_df[(items_df['price'] >= lower_bound) & (items_df['price'] <= upper_bound)]['price']
    
    fig, ax = plt.subplots(figsize=(6, 8))
    sns.boxplot(y=filtered_prices, color='orange', ax=ax)
    ax.set_title('Boxplot Distribusi Harga Item (Tanpa Outlier)', fontsize=14)
    ax.set_ylabel('Harga (BRL)', fontsize=12)
    st.pyplot(fig)

# Tren Penjualan
if "Tren Penjualan" in selected_sections:
    st.subheader("Tren Penjualan Harian, Mingguan, dan Bulanan")
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    orders_df['order_date'] = orders_df['order_purchase_timestamp'].dt.date
    orders_df['order_week'] = orders_df['order_purchase_timestamp'].dt.to_period('W').astype(str)
    orders_df['order_month'] = orders_df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    
    daily_trend = orders_df.groupby('order_date').size().head(30)
    weekly_trend = orders_df.groupby('order_week').size().head(10)
    monthly_trend = orders_df.groupby('order_month').size().head(12)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].plot(daily_trend.index, daily_trend.values, marker='o', linestyle='-', color='blue', alpha=0.7)
    axes[0].set_title('Tren Penjualan Harian')
    axes[0].set_xlabel('Tanggal')
    axes[0].set_ylabel('Jumlah Pesanan')
    axes[0].tick_params(axis='x', rotation=45)
    
    axes[1].plot(weekly_trend.index, weekly_trend.values, marker='o', linestyle='-', color='green', alpha=0.7)
    axes[1].set_title('Tren Penjualan Mingguan')
    axes[1].set_xlabel('Minggu')
    axes[1].set_ylabel('Jumlah Pesanan')
    axes[1].tick_params(axis='x', rotation=45)
    
    axes[2].plot(monthly_trend.index, monthly_trend.values, marker='o', linestyle='-', color='red', alpha=0.7)
    axes[2].set_title('Tren Penjualan Bulanan')
    axes[2].set_xlabel('Bulan')
    axes[2].set_ylabel('Jumlah Pesanan')
    axes[2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    st.pyplot(fig)

# Distribusi Penjualan Weekday vs Weekend
if "Distribusi Penjualan Weekday vs Weekend" in selected_sections:
    st.subheader("Distribusi Penjualan Berdasarkan Weekday dan Weekend")
    df = orders_df.copy()
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['day_of_week'] = df['order_purchase_timestamp'].dt.dayofweek
    df['order_category'] = df['day_of_week'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
    sales_by_category = df['order_category'].value_counts().reset_index()
    sales_by_category.columns = ['order_category', 'order_count']
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=sales_by_category, x='order_category', y='order_count', palette=['#1f77b4', '#ff7f0e'], ax=ax)
    ax.set_title('Distribusi Penjualan Berdasarkan Weekday dan Weekend', fontsize=14)
    ax.set_xlabel('Kategori Waktu', fontsize=12)
    ax.set_ylabel('Jumlah Pesanan', fontsize=12)
    st.pyplot(fig)


# Kategori Produk Terlaris
if "Kategori Produk Terlaris" in selected_sections:
    st.subheader("Top 10 Kategori Produk Terlaris")
    merged_products_df = items_df.merge(products_df[['product_id', 'product_category_name']], on='product_id', how='left')
    category_sales = merged_products_df['product_category_name'].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=category_sales.values, y=category_sales.index, palette='viridis', ax=ax)
    ax.set_title('Top 10 Kategori Produk Terlaris', fontsize=14)
    ax.set_xlabel('Jumlah Produk Terjual', fontsize=12)
    ax.set_ylabel('Kategori Produk', fontsize=12)
    st.pyplot(fig)


# Produk Terbaik Berdasarkan Review
if "Produk Terbaik Berdasarkan Review" in selected_sections:
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

    fig, ax = plt.subplots(figsize=(12, 6))
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
    st.pyplot(fig)


# Seller dengan Pendapatan Terbesar
if "Seller dengan Pendapatan Terbesar" in selected_sections:
    st.subheader("Top 10 Seller dengan Pendapatan Terbesar")
    merged_sellers_df = items_df.merge(payments_df[['order_id', 'payment_value']], on='order_id', how='left')
    seller_revenue = merged_sellers_df.groupby('seller_id').agg({'price': 'sum', 'freight_value': 'sum', 'payment_value': 'sum'})
    seller_revenue['total_revenue'] = seller_revenue['payment_value']
    top_sellers = seller_revenue.sort_values(by='total_revenue', ascending=False).head(10)
    top_sellers = top_sellers.merge(sellers_df[['seller_id', 'seller_city', 'seller_state']], on='seller_id', how='left')

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=top_sellers['total_revenue'], y=top_sellers['seller_id'], hue=top_sellers['seller_id'], palette='viridis', legend=False, ax=ax)
    ax.set_title('Top 10 Seller dengan Pendapatan Terbesar', fontsize=14)
    ax.set_xlabel('Total Pendapatan (BRL)', fontsize=12)
    ax.set_ylabel('Seller ID', fontsize=12)
    st.pyplot(fig)


# Conclusion
st.subheader("Conclusion")
st.markdown("""
- Metode pembayaran yang paling sering digunakan yaitu dengan kartu kredit sehingga dapat dilakukan promosi atau diskon jika transaksi menggunakan kartu kredit.
- Pelanggan paling banyak ada di provinsi SP (Sao Paulo). Kita bisa memberikan opsi untuk pengiriman di hari yang sama.
- Berdasarkan hasil visualisasi tren, kita bisa menekankan penjualan pada weekend untuk menambah market baru.
- Pada produk paling laris bisa diberikan beberapa jenis promo.
- Kategori produk yang tinggi berdasarkan rating bisa diprioritaskan pada halaman e-commerce.
- Seller dengan pendapatan paling besar bisa diapresiasi atau diberikan hadiah.
""")
