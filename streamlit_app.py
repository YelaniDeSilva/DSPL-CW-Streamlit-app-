import streamlit as st 
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
import os
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns  
import plotly.express as px

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

container1 = st.container()
col1, col2 = st.columns(2)


    
