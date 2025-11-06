# streamlit run dashboard.py
import streamlit as st
import pandas as pd
import altair as alt
from streamlit_autorefresh import st_autorefresh
import numpy as np

st.set_page_config(layout="wide")
st.markdown("""
    <h2 style='margin-top: -40px; margin-bottom: -35px; text-align: center; font-family: sans-serif; border-bottom: 2px dashed white;'>
        📊 Real-Time Propeller Dashboard
    </h2>
""", unsafe_allow_html=True)


# Refresh every second
st_autorefresh(interval=1000, key="datarefresh")

def load_data():
    try:
        return pd.read_csv("data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Power", "Voltage", "Sound", "Torque", "rpm", "Vibrations"])

df = load_data()
if df.empty:
    st.warning("Waiting for data…")
    st.stop()
    
# Reset index for plotting
df = df.reset_index().rename(columns={"index": "row_num"})
if len(df) >= 10:
    start, end = df.row_num.iloc[-10], df.row_num.iloc[-1]
elif len(df) > 0:
    start, end = df.row_num.iloc[0], df.row_num.iloc[-1]
else:
    start, end = 0, 1

# Function to create area charts
def make_area_chart(y_column, color, y_label): 
    return (
        alt.Chart(df)
        .mark_area(
            interpolate='monotone',
            opacity=0.65,
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    {"offset": 0, "color": color},
                    {"offset": 1, "color": "white"}
                ],
                x1=1, x2=1, y1=1, y2=0
            )
        )
        .encode(
            x=alt.X("row_num:Q", scale=alt.Scale(domain=[start, end]), title="Time (s)"),
            y=alt.Y(f"{y_column}:Q", title=y_label)
        )
        .properties(height=200)
        .interactive()
    )

# Metrics Row 1
m1, m2, m3 = st.columns(3)
m1.metric("Power", f"{df.Power.iloc[-1]} W")
m2.metric("Voltage", f"{df.Voltage.iloc[-1]} V")
m3.metric("Sound", f"{df.Sound.iloc[-1]} dB")
# Row 1: Power, Voltage, Sound
r1c1, r1c2, r1c3 = st.columns(3)
r1c1.altair_chart(make_area_chart("Power", "blue", "Power (W)"), use_container_width=True)
r1c2.altair_chart(make_area_chart("Voltage", "orange", "Voltage (V)"), use_container_width=True)
r1c3.altair_chart(make_area_chart("Sound", "green", "Sound (dB)"), use_container_width=True)

# Metrics Row 2
m4, m5, m6 = st.columns(3)
m4.metric("Torque", f"{df.Torque.iloc[-1]} Nm")
m5.metric("Rpm", f"{df.rpm.iloc[-1]} rpm")
m6.metric("Vibrations", f"{df.Vibrations.iloc[-1]} Hz")
# Row 2: Torque, rpm, Vibrations
r2c1, r2c2, r2c3 = st.columns(3)
r2c1.altair_chart(make_area_chart("Torque", "purple", "Torque (Nm)"), use_container_width=True)
r2c2.altair_chart(make_area_chart("rpm", "crimson", "rpm"), use_container_width=True)
r2c3.altair_chart(make_area_chart("Vibrations", "pink", "Vibrations (Hz)"), use_container_width=True)

# Modular Graphs Section
st.markdown("""
    <h3 style='margin-top: 40px; margin-bottom: 20px; text-align: center; font-family: sans-serif; border-bottom: 2px dashed white;'>
        📈 Modular Graphs
    </h3>
""", unsafe_allow_html=True)

colx, coly = st.columns(2)
x_axis = colx.selectbox("Select X-axis", df.columns[1:], index=0)
y_axis = coly.selectbox("Select Y-axis", df.columns[1:], index=1)

valx, valy = st.columns(2)
valx.metric(f"Current {x_axis}", f"{df[x_axis].iloc[-1]}")
valy.metric(f"Current {y_axis}", f"{df[y_axis].iloc[-1]}")

def plot_selected_axes(x, y):
    chart = (
        alt.Chart(df)
        .mark_line(interpolate='monotone', color='cyan')
        .encode(
            x=alt.X(f"{x}:Q", title=x, scale=alt.Scale(domain=[start, end])),
            y=alt.Y(f"{y}:Q", title=y)
        )
        .properties(
            height=300,
            title=f"{y} vs {x}"
        )
        .interactive()
    )
    return chart

st.altair_chart(plot_selected_axes(x_axis, y_axis), use_container_width=True)

# Expandable full data view
with st.expander("📋 Show full data"):
    st.dataframe(df[["Power", "Voltage", "Sound", "Torque", "rpm", "Vibrations"]])

# Completion/Error indicator
st.caption(f"📦 Current row count: {len(df)}")
if len(df) >= 80:
    st.success("✅ Data generation complete.")
