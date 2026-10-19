import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Diabetes Digital Twin", page_icon="🩺", layout="wide")

st.title("🩺 Diabetes Digital Twin")
st.caption("AI-powered glucose risk prediction | Research prototype using synthetic data")

st.info("This is a research demonstration, not a medical diagnosis.")

@st.cache_resource
def train_model():
    rng = np.random.default_rng(42)
    n = 3000
    glucose = rng.normal(145, 35, n).clip(65, 280)
    heart_rate = rng.normal(78, 12, n).clip(45, 130)
    sleep_hours = rng.normal(6.5, 1.5, n).clip(2, 12)
    steps = rng.integers(500, 12000, n)
    previous_glucose = glucose - rng.normal(0, 18, n)
    risk_score = (
        (glucose > 160).astype(int)
        + (previous_glucose > 150).astype(int)
        + (sleep_hours < 5).astype(int)
        + (steps < 2500).astype(int)
        + (heart_rate > 95).astype(int)
    )
    labels = (risk_score >= 2).astype(int)
    X = pd.DataFrame({
        "current_glucose": glucose,
        "previous_glucose": previous_glucose,
        "heart_rate": heart_rate,
        "sleep_hours": sleep_hours,
        "steps": steps,
    })
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, labels)
    return model

model = train_model()

st.subheader("Patient Digital Twin")
c1, c2, c3 = st.columns(3)

with c1:
    current_glucose = st.slider("Current glucose (mg/dL)", 60, 300, 155)
    previous_glucose = st.slider("Previous glucose (mg/dL)", 60, 300, 140)

with c2:
    heart_rate = st.slider("Heart rate (BPM)", 40, 140, 82)
    sleep_hours = st.slider("Sleep last night (hours)", 1.0, 12.0, 6.0, 0.5)

with c3:
    steps = st.slider("Steps today", 0, 20000, 3500, 500)
    patient_age = st.number_input("Patient age", 1, 110, 45)

patient = pd.DataFrame([{
    "current_glucose": current_glucose,
    "previous_glucose": previous_glucose,
    "heart_rate": heart_rate,
    "sleep_hours": sleep_hours,
    "steps": steps,
}])

risk = model.predict_proba(patient)[0][1]

st.divider()
st.subheader("Prediction Dashboard")
m1, m2, m3 = st.columns(3)
m1.metric("Current glucose", f"{current_glucose} mg/dL")
m2.metric("Heart rate", f"{heart_rate} BPM")
m3.metric("Model risk score", f"{risk:.0%}")

if risk >= 0.5:
    st.warning("Model flags a higher-risk pattern. This is not a validated prediction of a future glucose spike.")
else:
    st.success("Model flags a lower-risk pattern. This does not guarantee safety.")

st.subheader("Data streams combined")
st.write("**Historical/static inputs:** age and previous glucose reading.")
st.write("**Dynamic/sensor-style inputs:** current glucose, heart rate, sleep and daily steps.")
st.write("**Model:** Random Forest classifier trained on generated synthetic examples.")

chart_data = pd.DataFrame({
    "Measurement": ["Previous glucose", "Current glucose"],
    "mg/dL": [previous_glucose, current_glucose]
}).set_index("Measurement")
st.bar_chart(chart_data)

st.caption("Important: The displayed score is based on synthetic training data and is not clinically validated. It must not be used to make treatment decisions.")
