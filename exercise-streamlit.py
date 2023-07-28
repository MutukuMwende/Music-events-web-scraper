import streamlit as st
import plotly.express as px
import pandas as pd

data = pd.read_csv("data_ex.txt")

st.title("Plot")

temperature = data[" temperature"]
date = data["date"]


figure = px.line(x=date, y=temperature, labels={"x": "Date",
                                                "y": "Temperature (C)"})
st.plotly_chart(figure)


