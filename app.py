import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Telangana PDS Analytics",
    layout="wide"
)

st.title("Telangana PDS Analytics Dashboard")

df = pd.read_csv("final_clustered_dataset.csv")

st.write(df.head())
st.sidebar.header("Filters")

district = st.sidebar.selectbox(
    "District",
    sorted(df['distName'].dropna().unique())
)

filtered_df = df[
    df['distName'] == district
]
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Total Shops",
        filtered_df['shopNo'].nunique()
    )

with col2:
    st.metric(
        "Transactions",
        int(filtered_df['noOfTrans'].sum())
    )

with col3:
    st.metric(
        "Ration Cards",
        int(filtered_df['totalRcs'].sum())
    )

with col4:
    st.metric(
        "Anomalies",
        (filtered_df['dbscan_cluster']==-1).sum()
    )
    import plotly.express as px

fig = px.pie(
    filtered_df,
    names='cluster_name',
    title='Cluster Distribution'
)

st.plotly_chart(fig)
trend = (
    df.groupby('year_x')['otherShopTransCnt']
    .sum()
    .reset_index()
)

fig = px.line(
    trend,
    x='year_x',
    y='otherShopTransCnt',
    markers=True
)

st.plotly_chart(fig)
shop_no = st.text_input(
    "Enter Shop Number"
)

if shop_no:

    result = df[
        df['shopNo'].astype(str)==shop_no
    ]

    st.dataframe(result[
        [
            'shopNo',
            'cluster_name',
            'utilization_ratio',
            'portability_ratio',
            'dbscan_cluster'
        ]
    ])