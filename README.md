# Data Analysis Project
---
This project analyzes a public e-commerce dataset to extract meaningful business insights and answer critical business questions through data wrangling, exploratory analysis, and visualization.

## 📌 Business Questions
**1.** What is the most frequently used payment method?
**2.** Where are the majority of customers located?
**3.** What are the sales trends on a daily, weekly, and monthly basis?
**4.** Which product categories are best-selling?
**5.** Who are the top sellers based on revenue?
**6.** Which product categories receive the best customer reviews?

---
## 🧹 Data Wrangling
**1. Gathering**
The dataset contains null and missing values that need to be addressed.

**2. Assessing**
- Some columns contain missing data.
- Descriptive statistics were obtained using `.describe().`

**3. Cleaning**
- Missing datetime values were filled using the median after proper type conversion.
- Missing review titles/messages were filled with "No Title" and "No Message".
- Missing product category names were filled using the mode.
- Median imputation was used for numerical columns to minimize the impact of outliers.

## 📊 Exploratory Data Analysis (EDA)
- General descriptive statistics were explored.
- Categorical features were analyzed.
- Price distribution and inter-variable correlation were examined.
- The strongest correlation was between `payment_value` and `payment_installments`.

## 📈 Visualization & Explanatory Analysis
**Key Insights:**
- **Payment Method:** Credit card is the most popular payment method, likely due to convenience and promotional offers.
- **Customer Location:** Most customers are from São Paulo (SP), indicating a high concentration of e-commerce activity.
- **Sales Trends:** Sales tend to increase on weekdays and show monthly growth over the past year.
- **Best-Selling Categories:** *bed_table_bath (cama_mesa_banho)* is the most purchased product category.
- **Top Sellers:** The highest revenue-generating sellers consistently offer high-volume and high-value products.
- **Customer Satisfaction:** The *food* category receives the highest customer ratings.

## 📦 RFM (Recency, Frequency, Monetary) Analysis

This dataset is suitable for RFM analysis as it is transaction-based. The RFM model helps identify high-value customers for targeted marketing and retention strategies.
**RFM-Based Insights:**
- **Credit card** dominates as the primary payment method, showing dependence on digital payments.
- **São Paulo** holds the largest customer base, presenting a strong target market.
- Weekday transactions dominate, indicating purchase activity during work breaks.
- **bed_table_bath** is the top category, ideal for sellers aiming to boost sales.
- The best sellers likely implement effective strategies like discounts or premium services.
- The food category received the best reviews, signaling high customer satisfaction.

---

## 💡 Recommendations
- Promote digital payment usage (e.g., credit cards) to boost conversions.
- Focus marketing strategies in São Paulo while exploring potential in other regions.
- Align promotional campaigns with sales trends, such as offering discounts on weekdays.
- Encourage sellers to offer high-quality food products due to their strong customer feedback.

---

## Dashboard
You can access the dashboard right here:
<a href="https://dashboard-analysis-ecommerce.streamlit.app/" target="_blank"><img alt="Streamlit" src="https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white" /></a>    

or
```
https://dashboard-analysis-ecommerce.streamlit.app/
```

## Library
```
- Numpy
- Pandas
- Matplotlib
- Seaborn
- Streamlit
```

## Setup Environment
```
pip install -r requirements.txt
```

## Run steamlit app
```
cd dashboard
streamlit run dashboard.py
```

---

## 📁 Project Structure
```
📦 e-commerce-data-analysis
 ┣ 📊 dashboard/
 ┃ ┣ dashboard.py
 ┃ ┗ (clean_dataset)
 ┃
 ┣ 📁 data/
 ┃ ┣ customers_dataset.csv
 ┃ ┣ geolocation_dataset.csv
 ┃ ┣ order_items_dataset.csv
 ┃ ┣ order_payments_dataset.csv
 ┃ ┣ order_reviews_dataset.csv
 ┃ ┣ orders_dataset.csv
 ┃ ┣ product_category_name_translation.csv
 ┃ ┣ products_dataset.csv
 ┃ ┗ sellers_dataset.csv
 ┣ 🖥️ Data_Analysis_Project.ipynb
 ┣ 📄 README.md
 ┣ 📄 requirements.txt
 ┗ 📄 url.txt
 ```