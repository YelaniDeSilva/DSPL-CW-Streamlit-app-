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
uploaded_file = st.file_uploader("C:/Users/Asus/Downloads/education indicators.csv", type=["csv","xlsx"])

st.sidebar.header("Choose filters")