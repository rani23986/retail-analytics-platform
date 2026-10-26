import plotly.express as px

def monthly_revenue_chart(df):

    fig = px.line(
        df,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0,
        xaxis_title="Month",
        yaxis_title="Revenue (R$)",
        height=450
    )

    return fig

def top_categories_chart(df):

    fig = px.bar(
        df,
        x="revenue",
        y="category",
        orientation="h",
        title="Top Categories by Revenue"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0,
        xaxis_title="Revenue (R$)",
        yaxis_title="Category",
        height=450
    )

    fig.update_yaxes(categoryorder="total ascending")

    return fig

def top_sellers_chart(df):

    fig = px.bar(
        df,
        x="revenue",
        y="seller_id",
        orientation="h",
        title="Top Sellers by Revenue"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0,
        xaxis_title="Revenue (R$)",
        yaxis_title="Seller ID",
        height=450
    )

    fig.update_yaxes(categoryorder="total ascending")

    return fig