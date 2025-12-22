import streamlit as st
import pickle
import pandas as pd
import base64
import os

# =================================================
# Page Config (MUST be first Streamlit command)
# =================================================
st.set_page_config(
    page_title="Earthquake Magnitude Prediction",
    layout="centered"
)

# =================================================
# SAFE BACKGROUND IMAGE + FRONTEND STYLE
# =================================================
def apply_background_and_ui(image_path):
    try:
        if not os.path.exists(image_path):
            return  # Do nothing if image missing

        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        st.markdown(
            f"""
            <style>
            /* Full page background */
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                color: white;
            }}

            /* Dark overlay for readability */
            .stApp::before {{
                content: "";
                position: fixed;
                inset: 0;
                background: rgba(0, 0, 0, 0.7);
                z-index: -1;
            }}

            /* Title */
            h1 {{
                text-align: center;
                color: #00ffcc;
                font-weight: 700;
                margin-bottom: 30px;
            }}

            /* Labels */
            label {{
                color: #eaeaea !important;
                font-weight: 500;
            }}

            /* Input boxes */
            input {{
                background-color: rgba(0,0,0,0.75) !important;
                color: white !important;
                border: 1px solid #00ffcc !important;
                border-radius: 8px !important;
            }}

            /* +/- buttons */
            button[title="Increment"],
            button[title="Decrement"] {{
                background-color: #222 !important;
                color: white !important;
            }}

            /* Predict button */
            .stButton > button {{
                width: 100%;
                background: linear-gradient(90deg, #00ffcc, #00cc99);
                color: black;
                font-weight: bold;
                border-radius: 12px;
                padding: 0.7em;
                border: none;
                margin-top: 15px;
            }}

            /* Prediction output */
            .stSuccess {{
                background-color: rgba(0,0,0,0.85) !important;
                color: #00ffcc !important;
                border: 1px solid #00ffcc;
                border-radius: 12px;
                text-align: center;
                font-size: 18px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    except Exception:
        pass  # NEVER crash cloud app

# Apply background + UI
apply_background_and_ui("earthquake_bg.jpg")

# =================================================
# Load Model Pipeline (UNCHANGED)
# =================================================
with open("eq_dt_pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f)

# =================================================
# UI
# =================================================
st.title("🌍 Earthquake Magnitude Prediction")

latitude = st.number_input("Latitude", value=0.0)
longitude = st.number_input("Longitude", value=0.0)
depth = st.number_input("Depth (km)", value=0.0)
dmin = st.number_input("Dmin", value=0.0)
rms = st.number_input("RMS", value=0.0)
horizontalError = st.number_input("Horizontal Error", value=0.0)
depthError = st.number_input("Depth Error", value=0.0)

# =================================================
# Prediction (UNCHANGED)
# =================================================
if st.button("Predict"):
    input_df = pd.DataFrame(
        [[
            latitude,
            longitude,
            depth,
            dmin,
            rms,
            horizontalError,
            depthError
        ]],
        columns=[
            "latitude",
            "longitude",
            "depth",
            "dmin",
            "rms",
            "horizontalError",
            "depthError"
        ]
    )

    prediction = pipeline.predict(input_df)
    st.success(f"Predicted Magnitude: {prediction[0]:.2f}")




