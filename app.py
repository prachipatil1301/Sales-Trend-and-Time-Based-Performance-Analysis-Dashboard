import streamlit as st
import pandas as pd
import plotly.express as px

primary_color = "#6F4E37"   # coffee brown
secondary_color = "#C4A484" # latte beige
accent_color = "#2E8B57"    # green

st.set_page_config(
    page_title="Coffee Sales Dashboard",
    layout="wide"
)

st.title("☕ Sales Trend and Time-Based Performance Analysis for Afficionado Coffee Roasters")
#st.markdown("Analyze sales trends, demand patterns, and store performance")


df = pd.read_csv("afficionado_coffee_sales.csv")

df["transaction_time"] = pd.to_datetime(df["transaction_time"])

st.sidebar.header("Filters")

store_filter = st.sidebar.multiselect(
    "Select Store Location",
    options=df["store_location"].unique(),
    default=df["store_location"].unique()
)

hour_range = st.sidebar.slider(
    "Select Hour Range",
    min_value=int(df["hour"].min()),
    max_value=int(df["hour"].max()),
    value=(int(df["hour"].min()), int(df["hour"].max()))
)

metric = st.sidebar.radio(
    "Select Metric",
    ["revenue", "transaction_qty"]
)

category_filter = st.sidebar.multiselect(
    "Select Product Category",
    options=df["product_category"].unique(),
    default=df["product_category"].unique()
)

type_options = df[df["product_category"].isin(category_filter)]["product_type"].unique()

type_filter = st.sidebar.multiselect(
    "Select Product Type",
    options=type_options,
    default=type_options
)

detail_options = df[df["product_type"].isin(type_filter)]["product_detail"].unique()

detail_filter = st.sidebar.multiselect(
    "Select Product Detail",
    options=detail_options,
    default=detail_options
)

filtered_df = df[
    (df["store_location"].isin(store_filter)) &
    (df["hour"].between(hour_range[0], hour_range[1])) &
    (df["product_category"].isin(category_filter)) &
    (df["product_type"].isin(type_filter)) &
    (df["product_detail"].isin(detail_filter))
]

time_bucket_sales = filtered_df.groupby("time_bucket")[metric].sum().reset_index()

st.markdown("""
<style>
.kpi-card {
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
}

.kpi-title {
    font-size: 18px;
    color: #6F4E37;
}

.kpi-value {
    font-size: 28px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


total_revenue = filtered_df["revenue"].sum()
total_qty = filtered_df["transaction_qty"].sum()
total_transactions = filtered_df["transaction_id"].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Revenue</div>
        <div class="kpi-value">${total_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Quantity Sold</div>
        <div class="kpi-value">{total_qty:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Transactions</div>
        <div class="kpi-value">{total_transactions}</div>
    </div>
    """, unsafe_allow_html=True)

###########################

col1, col2 = st.columns(2)
trend = filtered_df.groupby("hour")[metric].sum().reset_index()

fig_trend = px.line(
    trend,
    x="hour",
    y=metric,
    markers=True,
    color_discrete_sequence=["#6F4E37"],
    title="Overall Sales Trend by Hour"
)

col1.plotly_chart(fig_trend, use_container_width=True)


hour_sales = filtered_df.groupby("hour")[metric].sum().reset_index()

fig_hour = px.bar(
    hour_sales,
    x="hour",
    y=metric,
    color_discrete_sequence=["#C4A484"]
)
col2.plotly_chart(fig_hour, use_container_width=True)

heatmap_data = filtered_df.pivot_table(
    values=metric,
    index="store_location",
    columns="hour",
    aggfunc="sum"
)

fig_heatmap = px.imshow(
    heatmap_data,
    color_continuous_scale="YlOrBr",
    title="Hourly Demand Heatmap"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

col3, col4 = st.columns(2)
location_sales = filtered_df.groupby("store_location")[metric].sum().reset_index()

fig_location = px.bar(
    location_sales,
    x="store_location",
    y=metric,
    color="store_location",
    color_discrete_sequence=["#6F4E37","#C4A484","#2E8B57"],
    title="Store Location Comparison"
)

col3.plotly_chart(fig_location, use_container_width=True)

category_sales = filtered_df.groupby("product_category")[metric].sum().reset_index()

fig_category = px.bar(
    category_sales,
    x="product_category",
    y=metric,
    color="product_category",
    color_discrete_sequence=["#6F4E37","#C4A484","#D2691E","#2E8B57"],
    title="Product Category Performance"
)

col4.plotly_chart(fig_category, use_container_width=True)

fig_time_bucket = px.bar(
    time_bucket_sales,
    x="time_bucket",
    y=metric,
    color="time_bucket",
    title="Coffee Demand Pattern by Time of Day",
    color_discrete_sequence=[
        "#6F4E37",
        "#C4A484",
        "#2E8B57",
        "#D2691E"
    ]
)

st.plotly_chart(fig_time_bucket, use_container_width=True)

bucket_order = ["Morning","Afternoon","Evening","Night"]

time_bucket_sales["time_bucket"] = pd.Categorical(
    time_bucket_sales["time_bucket"],
    categories=bucket_order,
    ordered=True
)

time_bucket_sales = time_bucket_sales.sort_values("time_bucket")

st.markdown("---")

st.markdown(
"""
<div style="text-align:center; font-size:14px;">
Created by Prachi Patil <br><br>

🔗 <a href="https://linkedin.com/in/prachi-patil-5a3a61392" target="_blank">LinkedIn</a> |
💻 <a href="https://github.com/prachipatil1301" target="_blank">GitHub</a>

</div>
""",
unsafe_allow_html=True
)
