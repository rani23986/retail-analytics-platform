import streamlit as st
import pandas as pd

from src.analytics.revenue import (
    get_total_revenue,
    get_top_categories,
    get_top_sellers,
    get_average_order_value,
    get_monthly_revenue
)
from src.analytics.customers import get_unique_customers, get_average_rating
from src.analytics.operations import (
    get_order_status_breakdown,
    get_delivery_performance,
    get_late_deliveries
)
from src.dashboard.charts import (
    monthly_revenue_chart,
    top_categories_chart,
    top_sellers_chart
)


st.set_page_config(
    page_title="Retail Analytics Platform",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛒 Retail Analytics Platform")
st.write("Welcome to the dashboard!")
st.caption("Executive Retail Performance Dashboard")
st.divider()


# ── Data fetching (all results are cached for 10 minutes) ─────────────────────
revenue = get_total_revenue()
top_categories = get_top_categories()
top_sellers = get_top_sellers()
average_order_value = get_average_order_value()
unique_customers = get_unique_customers()
average_rating = get_average_rating()
monthly_revenue = get_monthly_revenue()
monthly_revenue = monthly_revenue.iloc[:-2]

delivery_perf = get_delivery_performance()
late_deliveries = get_late_deliveries()

monthly_revenue["month"] = (
    pd.to_datetime(monthly_revenue["month"])
      .dt.strftime("%b %Y")
)


# ── KPI Row ───────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"R$ {revenue.iloc[0, 0] / 1_000_000:.2f} M"
    )

with col2:
    st.metric(
        "👥 Unique Customers",
        f"{unique_customers.iloc[0, 0]:,}"
    )

with col3:
    st.metric(
        "⭐ Avg Rating",
        f"{average_rating.iloc[0, 0]} / 5"
    )

with col4:
    st.metric(
        "🛒 Avg Order Value",
        f"R$ {average_order_value.iloc[0, 0]:,.2f}"
    )

st.divider()

# ── Monthly Revenue Trend ─────────────────────────────────────────────────────
st.subheader("📈 Monthly Revenue Trend")

st.plotly_chart(
    monthly_revenue_chart(monthly_revenue),
    use_container_width=True
)

highest_month = monthly_revenue.loc[monthly_revenue["revenue"].idxmax()]

st.caption(
    f"📌 Highest Revenue Month: **{highest_month['month']}** "
    f"(R$ {highest_month['revenue']:,.2f})"
)

with st.expander("View Raw Data"):
    st.dataframe(monthly_revenue, use_container_width=True)

st.divider()

# ── Category & Seller Performance ────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.subheader("🛍 Top Categories")
    st.plotly_chart(
        top_categories_chart(top_categories),
        use_container_width=True
    )
    highest_category = top_categories.iloc[0]
    st.caption(
        f"📌 Highest Revenue Category: **{highest_category['category']}** "
        f"(R$ {highest_category['revenue']:,.2f})"
    )
    with st.expander("View Raw Data"):
        st.dataframe(top_categories, use_container_width=True)

with right:
    st.subheader("🏪 Top Sellers")
    st.plotly_chart(
        top_sellers_chart(top_sellers),
        use_container_width=True
    )
    highest_seller = top_sellers.iloc[0]
    st.caption(
        f"📌 Highest Revenue Seller: **{highest_seller['seller_id']}** "
        f"(R$ {highest_seller['revenue']:,.2f})"
    )
    with st.expander("View Raw Data"):
        st.dataframe(top_sellers, use_container_width=True)

st.divider()

# ── Operations & Delivery ─────────────────────────────────────────────────────
st.subheader("🚚 Operations & Delivery Performance")

op1, op2, op3 = st.columns(3)

avg_actual = delivery_perf.iloc[0]["avg_actual_delivery_days"]
avg_estimated = delivery_perf.iloc[0]["avg_estimated_delivery_days"]
late_pct = late_deliveries.iloc[0]["late_pct"]

with op1:
    st.metric("📦 Avg Actual Delivery", f"{avg_actual} days")

with op2:
    st.metric("🗓 Avg Estimated Delivery", f"{avg_estimated} days")

with op3:
    st.metric("⚠️ Late Delivery Rate", f"{late_pct}%")

order_status = get_order_status_breakdown()

with st.expander("Order Status Breakdown"):
    st.dataframe(order_status, use_container_width=True)

st.divider()

# ── Business Summary ──────────────────────────────────────────────────────────
st.subheader("💡 Business Summary")

st.success(f"""
**Highest Revenue Month:**  
{highest_month['month']} (R$ {highest_month['revenue']:,.2f})

**Highest Revenue Category:**  
{highest_category['category']} (R$ {highest_category['revenue']:,.2f})

**Highest Revenue Seller:**  
{highest_seller['seller_id'][:8]}... (R$ {highest_seller['revenue']:,.2f})

**Delivery:**  
{late_pct}% of orders were delivered late ({avg_actual} days avg vs {avg_estimated} days estimated)
""")

with st.container():
    st.write("**AI-based Recommendations:**  Coming Soon 🚀")

st.divider()

st.caption(
    "Retail Analytics Platform | Built with Python • MySQL • Streamlit • Plotly"
)
