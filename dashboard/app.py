import streamlit as st
import plotly.express as px
from utils.load_data import load_data

st.set_page_config(
    page_title="Deaz & Co Analytics",
    page_icon="📊",
    layout="wide"
)

df = load_data()

#sidebar

st.sidebar.markdown("""
<h2 style='text-align:center;
color:#22C55E;
margin-bottom:0px;'>

🔎 FILTER

</h2>

<hr style="
height:2px;
border:none;
background:#22C55E;
margin-top:10px;
margin-bottom:20px;
">

""", unsafe_allow_html=True)





#filter tahun
years = sorted(df["Order Date"].dt.year.unique())

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    years,
    default=years
)

#filter region
regions = sorted(df["Region"].unique())

selected_region = st.sidebar.multiselect(
    "Pilih Region",
    regions,
    default=regions
)


#filter category
categories = sorted(df["Category"].unique())

selected_category = st.sidebar.multiselect(
    "Pilih Category",
    categories,
    default=categories
)

#filter segment
segments = sorted(df["Segment"].unique())

selected_segment = st.sidebar.multiselect(
    "Pilih Segment",
    segments,
    default=segments
)


#filter data
df = df[
    (df["Order Date"].dt.year.isin(selected_year)) &
    (df["Region"].isin(selected_region)) &
    (df["Category"].isin(selected_category)) &
    (df["Segment"].isin(selected_segment))
]

st.sidebar.markdown("---")


st.sidebar.markdown("""
### 📄 Dataset

**Source**

Deaz & Co Analytics

**Period**

2011 - 2014
""")



st.markdown("""
<h1 style='text-align: center;
color: white;
font-size:48px;
margin-bottom:0px;'>

DEAZ & CO

</h1>

<h3 style='text-align: center;
color:#22C55E;
margin-top:0px;'>

Executive Business Dashboard

</h3>

<p style='text-align:center;
font-size:18px;
color:gray;'>

Sales Analytics • Business Performance • Profitability

</p>

<hr style="margin-top:10px;margin-bottom:25px;">

""", unsafe_allow_html=True)

st.markdown("""
<hr style="
height:2px;
border:none;
background:linear-gradient(to right,#22C55E,#3B82F6);
margin-top:20px;
margin-bottom:30px;
">
""", unsafe_allow_html=True)

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_order = len(df)
avg_discount = df["Discount"].mean()

#buat 4 kolom

col1, col2, col3, col4 = st.columns(4)

#isi KPI

col1.metric(
    "💰 Total Sales",
    f"Rp {total_sales:,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"Rp {total_profit:,.0f}"
)

col3.metric(
    "🛒 Total Orders",
    f"{total_order:,}"
)

col4.metric(
    "🏷 Average Discount",
    f"{avg_discount:.1%}"
)

st.markdown("---")

st.subheader("Dataset Preview")

st.dataframe(df.head())


#Sales Trend (Plotly)

sales_trend = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
      .sum()
      .reset_index()
)

sales_trend["Order Date"] = sales_trend["Order Date"].astype(str)

fig = px.line(
    sales_trend,
    x="Order Date",
    y="Sales",
    title="📈 Sales Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

left, right = st.columns(2)

#salec category
sales_category = (
    df.groupby("Category")["Sales"]
      .sum()
      .reset_index()
)

fig_sales = px.bar(
    sales_category,
    x="Category",
    y="Sales",
    title="Sales by Category"
)

left.plotly_chart(
    fig_sales,
    use_container_width=True
)


#profit category
profit_category = (
    df.groupby("Category")["Profit"]
      .sum()
      .reset_index()
)

fig_profit = px.bar(
    profit_category,
    x="Category",
    y="Profit",
    title="Profit by Category"
)

right.plotly_chart(
    fig_profit,
    use_container_width=True
)

left, right = st.columns(2)

#sales by region

sales_region = (
    df.groupby("Region")["Sales"]
      .sum()
      .reset_index()
)

fig_region = px.bar(
    sales_region,
    x="Region",
    y="Sales",
    title="🌍 Sales by Region",
    color="Region"
)

left.plotly_chart(
    fig_region,
    use_container_width=True
)


#sales by segment
sales_segment = (
    df.groupby("Segment")["Sales"]
      .sum()
      .reset_index()
)

fig_segment = px.pie(
    sales_segment,
    names="Segment",
    values="Sales",
    title="👥 Sales by Segment"
)

right.plotly_chart(
    fig_segment,
    use_container_width=True
)


#top 10 products
top_product = (
    df.groupby("Product Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig_top = px.bar(
    top_product,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="🏆 Top 10 Product by Sales"
)

st.plotly_chart(
    fig_top,
    use_container_width=True
)


# Discount and Profit
fig_discount = px.scatter(
    df,
    x="Discount",
    y="Profit",
    title="💰 Discount vs Profit",
    hover_data=["Product Name", "Category"]
)

fig_discount.update_layout(
    xaxis_title="Discount",
    yaxis_title="Profit",
    xaxis=dict(
        tickformat=".0%"
    )
)

st.plotly_chart(
    fig_discount,
    use_container_width=True
)
# Average Profit by Discount
discount_profit = df.groupby("Discount").agg(
    Avg_Profit=("Profit", "mean"),
    Total_Profit=("Profit", "sum"),
    Transactions=("Profit", "count")
).reset_index()

fig_avg_discount = px.line(
    discount_profit,
    x="Discount",
    y="Avg_Profit",
    markers=True,
    title="📊 Average Profit by Discount"
)

fig_avg_discount.update_layout(
    xaxis_title="Discount",
    yaxis_title="Average Profit",
    xaxis=dict(
        tickformat=".0%"
    )
)

st.plotly_chart(fig_avg_discount, use_container_width=True)



df = load_data()

# =========================
# TOP 10 CUSTOMERS
# =========================

# Top 10 Customer by Revenue
top_customers = (
    df.groupby("Customer Name", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
)

# Convert Revenue to Million
top_customers["Revenue_M"] = top_customers["Sales"] / 1_000_000


# Top 10 Customer by Order Frequency
top_customers_frequency = (
    df.groupby("Customer Name")["Order ID"]
    .nunique()
    .reset_index(name="Order Frequency")
    .sort_values("Order Frequency", ascending=False)
    .head(10)
)


st.subheader("Top 10 Customers")

col1, col2 = st.columns(2)


# ==========================================
# LEFT — TOP 10 BY REVENUE
# ==========================================

with col1:

    st.markdown("### 💰 Top 10 by Revenue")

    fig_revenue = px.bar(
        top_customers.sort_values("Revenue_M"),
        x="Revenue_M",
        y="Customer Name",
        orientation="h",
        text="Revenue_M"
    )

    fig_revenue.update_traces(
        texttemplate="Rp %{x:.1f}M",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Revenue: Rp %{x:.1f}M<extra></extra>"
    )

    fig_revenue.update_layout(
        xaxis_title="Revenue (Million IDR)",
        yaxis_title="",
        height=500,
        showlegend=False
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True
    )


# ==========================================
# RIGHT — TOP 10 BY ORDER FREQUENCY
# ==========================================

with col2:

    st.markdown("### 🔄 Top 10 by Order Frequency")

    fig_frequency = px.bar(
        top_customers_frequency.sort_values("Order Frequency"),
        x="Order Frequency",
        y="Customer Name",
        orientation="h",
        text="Order Frequency"
    )

    fig_frequency.update_traces(
        texttemplate="%{x} orders",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Orders: %{x}<extra></extra>"
    )

    fig_frequency.update_layout(
        xaxis_title="Number of Orders",
        yaxis_title="",
        height=500,
        showlegend=False
    )

    st.plotly_chart(
        fig_frequency,
        use_container_width=True
    )




st.markdown("---")

st.markdown("""
<div style="
    background:#1E3A5F;
    padding:20px;
    border-radius:10px;
">

<h4 style="color:white;">💡 Business Insight</h4>

<ul style="color:white; line-height:1.8;">

<li><b>Pertumbuhan penjualan yang konsisten selama periode 2011–2014</b> menunjukkan bahwa bisnis memiliki kinerja yang terus berkembang. Perusahaan dapat mempertahankan strategi yang telah berjalan sambil menyiapkan kapasitas operasional untuk mendukung pertumbuhan di tahun-tahun berikutnya.</li>

<li><b>Kategori Furniture menjadi kontributor profit terbesar</b>, sehingga layak diprioritaskan dalam strategi bisnis melalui optimalisasi stok, promosi, dan pengembangan variasi produk untuk meningkatkan kontribusi keuntungan.</li>

<li><b>Wilayah Barat memberikan kontribusi penjualan tertinggi</b>. Perusahaan dapat menjadikan wilayah ini sebagai benchmark dalam strategi pemasaran serta mengidentifikasi peluang untuk meningkatkan performa wilayah Tengah dan Timur.</li>

<li><b>Hubungan antara diskon dan profit tergolong sangat lemah</b>, sehingga peningkatan profit tidak dapat dicapai hanya dengan mengubah kebijakan diskon. Evaluasi terhadap harga jual, margin produk, dan komposisi produk lebih berpotensi memberikan dampak terhadap profitabilitas.</li>

<li><b>Penjualan bulanan masih berfluktuasi</b> meskipun tren tahunan terus meningkat. Kondisi ini mengindikasikan adanya faktor musiman atau perubahan permintaan pasar yang perlu dipertimbangkan dalam perencanaan promosi dan pengelolaan persediaan.</li>

</ul>

</div>
""", unsafe_allow_html=True)






st.sidebar.markdown("---")

st.sidebar.caption("""
Developed by **Deaz Tobing**

Powered by Streamlit & Plotly
""")