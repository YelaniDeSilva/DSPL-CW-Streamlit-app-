import streamlit as st 
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
import os
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns  
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Streamlit dashboard",layout="wide")

st.title("Education indicators for Sri Lanka ")

df= pd.read_csv("education indicators.csv")

st.sidebar.header("Choose filters")
# Create for Age range 
age_range = st.sidebar.multiselect("Select an age range", df["Age range "].unique())
if not age_range:
    df2 = df.copy()
else:
    df2 = df[df["Age range "].isin(age_range)]

#Create for year
year = st.sidebar.multiselect("Select an year", df2["Year"].unique())
if not year:
    df3 = df2.copy()
else:
    df3 = df2[df2["Year"].isin(year)]

#Create for indicators 
indicators = st.sidebar.multiselect("Pick an indicator",df3["Indicator "].unique())

# Filter the data based on age range, year and indicators

if not age_range and not year and not indicators:
    filtered_df = df
elif not year and not indicators:
    filtered_df = df[df["Age range "].isin(age_range)]
elif not age_range and not indicators:
    filtered_df = df[df["Year"].isin(year)]
elif year and indicators:
    filtered_df = df3[df["Year"].isin(year) & df3["Indicator "].isin(indicators)]
elif age_range and indicators:
    filtered_df = df3[df["Age range "].isin(age_range) & df3["Indicator "].isin(indicators)]
elif age_range and year:
    filtered_df = df3[df["Age range "].isin(age_range) & df3["Year"].isin(year)]
elif indicators:
    filtered_df = df3[df3["Indicator "].isin(indicators)]
else:
    filtered_df = df3[df3["Age range "].isin(age_range) & df3["Year"].isin(year) & df3["Indicator "].isin(indicators)]

#creating columns and a container
container1 = st.container()
col1, col2 = st.columns(2)

import streamlit as st
import plotly.graph_objects as go

# Create columns and container
container1 = st.container()
col1, col2 = st.columns(2)

with col1:
    color_mapping = {
        "SEC.CMPT": 'indianred',      
        "PRM.CMPT": 'forestgreen',      
        "NOED": 'royalblue',       
        "TER.CMPT": 'mediumorchid'     
    }

    legend_label_mapping = {
        "SEC.CMPT": "Secondary education",
        "PRM.CMPT": "Primary education",
        "NOED": "No education",
        "TER.CMPT": "Tertiary education"
    }

    avg_by_code = filtered_df.groupby("Indicator Code")["Value"].mean().reset_index()
    avg_by_code = avg_by_code.sort_values(by="Value", ascending=False)

    st.subheader("Average values by indicator code")

    avg_by_code["Color"] = avg_by_code["Indicator Code"].map(color_mapping).fillna('lightgray')

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=avg_by_code["Indicator Code"],
        y=avg_by_code["Value"],
        marker_color=avg_by_code["Color"],
        showlegend=False,
        width=0.4
    ))

    for code, color in color_mapping.items():
        fig.add_trace(go.Bar(
            x=[None], y=[None],
            marker=dict(color=color),
            name=legend_label_mapping.get(code, code),
            showlegend=True
        ))

    fig.update_layout(
        height=400,
        font=dict(size=13),
        margin=dict(t=40, b=40, l=40, r=40),
        xaxis=dict(title="Indicator Code", tickangle=45),
        yaxis=dict(title="Average Percentage Value"),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1,
            borderwidth=1
        ),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Average values by age range")

    avg_by_age = filtered_df.groupby("Age range ")["Value"].mean().reset_index()
    avg_by_age = avg_by_age.sort_values(by="Value", ascending=False)

    age_color_mapping = {
        "15-19": "indianred",
        "20-24": "forestgreen",
        "25-29": "blueviolet",
        "30-34": "mediumorchid",
        "35-39": "yellow",
        "40-44": "royalblue",
        "45-49": "olivedrab"
    }

    avg_by_age["Color"] = avg_by_age["Age range "].map(age_color_mapping).fillna("lightgray")

    pie_fig = go.Figure()

    pie_fig.add_trace(go.Pie(
        labels=avg_by_age["Age range "],
        values=avg_by_age["Value"],
        marker=dict(colors=avg_by_age["Color"]),
        textinfo='percent+label',
        insidetextorientation='radial',
        showlegend=False
    ))

    for idx, row in avg_by_age.iterrows():
        pie_fig.add_trace(go.Bar(
            x=[None], y=[None],
            marker=dict(color=row["Color"]),
            name=row["Age range "],
            showlegend=True
        ))

    pie_fig.update_layout(
        height=320,
        font=dict(size=13),
        margin=dict(t=40, b=40, l=40, r=40),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1,
            borderwidth=1
        ),
        showlegend=True
    )

    st.plotly_chart(pie_fig, use_container_width=True, key="Age range average")

# Create new container
container2 = st.container()
col3, col4 = st.columns(2)

with col3:
    st.subheader("Average values by year")

    avg_by_year = filtered_df.groupby("Year")["Value"].mean().reset_index()
    avg_by_year = avg_by_year.sort_values(by="Year")

    line_fig = go.Figure()

    line_fig.add_trace(go.Scatter(
        x=avg_by_year["Year"],
        y=avg_by_year["Value"],
        mode='lines+markers',
        line=dict(color='lightskyblue', width=2),
        marker=dict(size=6),
        name="Average %"
    ))

    line_fig.update_layout(
        height=400,
        font=dict(size=13),
        margin=dict(t=40, b=40, l=40, r=40),
        xaxis=dict(
            title="Year",
            showgrid=False,
            tickmode='array',
            tickvals=avg_by_year["Year"]
        ),
        yaxis=dict(
            title="Average Percentage Value",
            showgrid=True
        )
    )

    st.plotly_chart(line_fig, use_container_width=True, key="line chart by year")

with col4:
    st.subheader("Distribution of average values by year")

    avg_by_year = filtered_df.groupby("Year")["Value"].mean().reset_index()
    avg_by_year = avg_by_year.sort_values(by="Year")

    hist_fig = go.Figure()

    hist_fig.add_trace(go.Bar(
        x=avg_by_year["Year"],
        y=avg_by_year["Value"],
        marker_color='deepskyblue',
        width=4.9,
        name="Avg % per Year"
    ))

    hist_fig.update_layout(
        height=400,
        font=dict(size=13),
        margin=dict(t=40, b=40, l=40, r=40),
        xaxis=dict(
            title=dict(text="Year"),
            tickvals=avg_by_year["Year"],
        ),
        yaxis=dict(
            title=dict(text="Average Percentage Value"),
        ),
        bargap=0.05
    )

    st.plotly_chart(hist_fig, use_container_width=True, key="histogram by year")

# Grouped bar chart 
# Color and label mapping
color_mapping = {
    "SEC.CMPT": 'indianred',
    "PRM.CMPT": 'forestgreen',
    "NOED": 'royalblue',
    "TER.CMPT": 'mediumorchid'
}

legend_label_mapping = {
    "SEC.CMPT": "Secondary education",
    "PRM.CMPT": "Primary education",
    "NOED": "No education",
    "TER.CMPT": "Tertiary education"
}

# Group by Year and Indicator Code
grouped = filtered_df.groupby(["Year", "Indicator Code"])["Value"].mean().reset_index()

# Pivot table
pivot_df = grouped.pivot(index="Year", columns="Indicator Code", values="Value").reset_index()

all_years = sorted(filtered_df["Year"].unique())
pivot_df = pivot_df.set_index("Year").reindex(all_years).reset_index()


st.subheader("Grouped average values by year and education indicators")
fig = go.Figure()

for code, color in color_mapping.items():
    if code in pivot_df.columns:
        fig.add_trace(go.Bar(
            x=pivot_df["Year"],
            y=pivot_df[code],
            name=legend_label_mapping[code],
            marker_color=color
        ))

fig.update_layout(
    barmode='group',  
    height=500,
    font=dict(size=13),
    xaxis=dict(
        title="Year",
        tickmode='array',
        tickvals=pivot_df["Year"],  
    ),
    yaxis=dict(title="Average Percentage Value"),
    legend=dict(
        title="Education Level",
        x=1,
        xanchor="left",
        y=1,
        bgcolor="rgba(0,0,0,0)",  
    ),
    margin=dict(t=40, b=40, l=40, r=40)
)

st.plotly_chart(fig, use_container_width=True)









