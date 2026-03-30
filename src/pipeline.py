import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

df_item = pd.read_csv(DATA_RAW / "olist_order_items_dataset.csv")
df_reviews = pd.read_csv(DATA_RAW / "olist_order_reviews_dataset.csv")
df_orders = pd.read_csv(DATA_RAW / "olist_orders_dataset.csv")
df_products = pd.read_csv(DATA_RAW / "olist_products_dataset.csv")
df_geolocation = pd.read_csv(DATA_RAW / "olist_geolocation_dataset.csv")
df_sellers = pd.read_csv(DATA_RAW / "olist_sellers_dataset.csv")
df_order_pay = pd.read_csv(DATA_RAW / "olist_order_payments_dataset.csv")
df_customers = pd.read_csv(DATA_RAW / "olist_customers_dataset.csv")
df_category = pd.read_csv(DATA_RAW / "product_category_name_translation.csv")

df_item_clean = df_item.copy()
df_reviews_clean = df_reviews.copy()
df_orders_clean = df_orders.copy()
df_products_clean = df_products.copy()
df_geolocation_clean = df_geolocation.copy()
df_sellers_clean = df_sellers.copy()
df_order_pay_clean = df_order_pay.copy()
df_customers_clean = df_customers.copy()
df_category_clean = df_category.copy()


# df_orders date_time treatment

df_orders_clean['order_purchase_timestamp'] = pd.to_datetime(df_orders_clean['order_purchase_timestamp'])
df_orders_clean['order_approved_at'] = pd.to_datetime(df_orders_clean['order_approved_at'])
df_orders_clean['order_delivered_carrier_date'] = pd.to_datetime(df_orders_clean['order_delivered_carrier_date'])
df_orders_clean['order_delivered_customer_date'] = pd.to_datetime(df_orders_clean['order_delivered_customer_date'])
df_orders_clean['order_estimated_delivery_date'] = pd.to_datetime(df_orders_clean['order_estimated_delivery_date'])

# df_reviews date_time treatment

df_reviews_clean['review_creation_date'] = pd.to_datetime(df_reviews_clean['review_creation_date'])
df_reviews_clean['review_answer_timestamp'] = pd.to_datetime(df_reviews_clean['review_answer_timestamp'])

# df_customers treatment

df_customers_clean["customer_state"] = df_customers_clean["customer_state"].astype("category")

# df_item date_time treatment

df_item_clean["shipping_limit_date"] = pd.to_datetime(df_item_clean["shipping_limit_date"])

# df_products date_time treatment

df_products_clean['product_weight_g'] = pd.to_numeric(df_products_clean['product_weight_g'], errors='coerce')
df_products_clean['product_length_cm'] = pd.to_numeric(df_products_clean['product_length_cm'], errors='coerce')
df_products_clean['product_height_cm'] = pd.to_numeric(df_products_clean['product_height_cm'], errors='coerce')
df_products_clean['product_width_cm'] = pd.to_numeric(df_products_clean['product_width_cm'], errors='coerce')

# df_sellers treatment

df_sellers_clean["seller_state"] = df_sellers_clean["seller_state"].astype("category")

# df_order_pay date_time treatment

df_order_pay_clean['payment_sequential'] = pd.to_numeric(df_order_pay_clean['payment_sequential'], errors='coerce')
df_order_pay_clean['payment_installments'] = pd.to_numeric(df_order_pay_clean['payment_installments'], errors='coerce')
df_order_pay_clean['payment_value'] = pd.to_numeric(df_order_pay_clean['payment_value'], errors='coerce')

main_df = df_orders_clean.copy()
main_df = df_orders_clean.merge(df_customers_clean, on="customer_id", how="left")
main_df = main_df.merge(df_item_clean, on="order_id", how="left")
main_df = main_df.merge(df_products_clean, on="product_id", how="left")
main_df = main_df.merge(df_sellers_clean, on="seller_id", how="left")


# Product Dimension
dim_product = df_products_clean[['product_id','product_category_name','product_weight_g','product_length_cm']].drop_duplicates()

# Customer Dimension
dim_customer = df_customers_clean[['customer_id','customer_state','customer_zip_code_prefix']].drop_duplicates()

# Seller Dimension
dim_seller = df_sellers_clean[['seller_id','seller_state']].drop_duplicates()




#FACT_ORDERS 
fact_orders = df_orders_clean.merge(df_item_clean, on='order_id') \
                             .merge(df_products_clean[['product_id','product_category_name']], on='product_id', how='left') \
                             .merge(df_order_pay_clean, on='order_id', how='left')

fact_orders['order_value'] = fact_orders['price'] + fact_orders['freight_value']
fact_orders['delivery_time'] = (fact_orders['order_delivered_customer_date'] - fact_orders['order_purchase_timestamp']).dt.days

fact_orders = fact_orders[['order_id','customer_id','product_id','seller_id','product_category_name','order_value','delivery_time','payment_value']]

# To find nulls values

'''for name, df in {
"orders": df_orders,
"items": df_item,
"products": df_products,
"customers": df_customers,
"payments": df_order_pay,
"reviews": df_reviews
}.items():
print("\n", name)
print(df.isnull().sum())'''

# Analiticals Variables

main_df["delivery_time"] = (
main_df["order_delivered_customer_date"] -
main_df["order_purchase_timestamp"]
).dt.days

main_df["delivery_delay"] = fact_orders["delivery_time"] - (
main_df["order_estimated_delivery_date"] - main_df["order_purchase_timestamp"]).dt.days

main_df["purchase_month"] = main_df["order_purchase_timestamp"].dt.month

main_df.isnull().sum().sort_values(ascending=False)

#KPI's
main_df['order_value'] = main_df['price'] + main_df['freight_value']

total_revenue = main_df.groupby('order_id')['order_value'].sum().sum()

total_orders = main_df['order_id'].nunique()

ticket_medio = df_order_pay.groupby('order_id')['payment_value'].sum().mean()

cancel_rate = (df_orders[df_orders['order_status']=='canceled']['order_id'].nunique() /df_orders['order_id'].nunique())

avg_delivery_time = main_df['delivery_time'].mean()

avg_delivery_delay = main_df['delivery_delay'][main_df['delivery_delay'] > 0].mean()

repeat_customers = main_df.groupby('customer_id')['order_id'].nunique()

repeat_rate = (repeat_customers > 1).sum() / main_df['customer_id'].nunique()

revenue_by_category = fact_orders.groupby('product_category_name')['payment_value'].sum().sort_values(ascending=False)

# Cleaned CSVs

main_df.to_csv(DATA_PROCESSED / "clean_olist.csv", index=False)

dim_seller.to_csv(DATA_PROCESSED / "olist_dim_seller.csv", index=False)
dim_product.to_csv(DATA_PROCESSED / "olist_dim_product.csv", index=False)
dim_customer.to_csv(DATA_PROCESSED / "olist_dim_customer.csv", index=False)

#FACT_PAYMENTS
df_order_pay_clean.to_csv(DATA_PROCESSED / "olist_fact_payments.csv", index=False)

#FACT_REVIEWS
df_reviews_clean.to_csv(DATA_PROCESSED / "olist_fact_reviews.csv", index=False)

#FACT_ORDERS 
fact_orders.to_csv(DATA_PROCESSED / "olist_fact_orders.csv", index=False)
# Backup 
main_df.to_csv(DATA_PROCESSED / "backup_main_df.csv", index=False)
