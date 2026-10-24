import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = Path("data/trips.db")

st.title("OBD Telematics Dashboard")

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM readings", conn)

trips_df = pd.read_sql_query("SELECT * FROM trips", conn)
chosen_trip = st.selectbox("Pick a trip" , trips_df["id"])
filtered = df[df["trip_id"] == chosen_trip]

st.dataframe(filtered)
conn.close()