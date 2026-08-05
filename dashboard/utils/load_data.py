import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("dataset/Deaz Co Analytics Clean.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df