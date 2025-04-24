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
    
