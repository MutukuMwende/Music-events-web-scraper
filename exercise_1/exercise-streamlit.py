import streamlit as st
import plotly.express as px
import sqlite3

connection = sqlite3.connect("data_ex.db")
cursor = connection.cursor()

st.title("Plot")

cursor.execute("SELECT Temperature FROM Temperatures")
temperature = cursor.fetchall()
temperature = [item[0] for item in temperature]

cursor.execute("SELECT Date FROM Temperatures")
date = cursor.fetchall()
date = [item[0] for item in date]

figure = px.line(x=date, y=temperature, labels={"x": "Date",
                                                "y": "Temperature (C)"})
st.plotly_chart(figure)


