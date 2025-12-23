import streamlit as st
import pickle
import pandas as pd
import base64
import os

# =================================================
# PAGE CONFIG (MUST BE FIRST)
# =================================================
st.set_page_config(
    page_title="Earthquake Magnitude Prediction",
    layout="centered"
)

# =================================================
# BACKGROUND + UI STYLING
# =================================================
def apply_background_and_ui(image_path):
    try:
        if not os.path.exists(image_path):
            return

        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        st.markdown(
            f"""
            <style>
            /* App background */
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                color: white;
            }}

            /* Dark overlay */
            .stApp::before {{
                content: "";
                position: fixed;
                inset: 0;
                background: rgba(0, 0, 0, 0.75);
                z-index: -1;
            }}

            /* Center card */
            .block-container {{
                background: rgba(0, 0, 0, 0.78);
                padding: 2rem 2.5rem;
                border-radius: 18px;
                max-width: 520px;
                margin-top: 60px;
                box-shadow: 0 0 25px rgba(0,255,204,0.25);
            }}

            /* Title */
            h1 {{
                text-align: center;
                color: #00ffcc;
                font-weight: 800;
                margin-bottom: 30px;
            }}

            /* Labels */
            label {{
                color: #ffffff !important;
                font-weight: 600 !important;
                font-size: 14px !important;
            }}

            /* Inputs */
            input {{
                background-color: rgba(0,0,0,0.9) !important;
                color: white !important;
                border: 1px solid #00ffcc !important;
                border-radius: 8px !important;
            }}

            input::placeholder {{
                color: #cccccc !important;
            }}

            /* +/- buttons */
            button[title="Increment"],
            button[title="Decrement"] {{
                background-color: #111 !important;
                color: #00ffcc !important;
                border: 1px solid #00ffcc !important;
            }}

            /* Predict button */
            .stButton > button {{
                width: 100%;
                background: linear-gradient(90deg, #00ffcc, #00cc99);
                color: black;
                font-weight: bold;
                border-radius: 12px;
                padding: 0.8em;
                border: none;
                margin-top: 20px;
                font-size: 16px;
            }}

            /* Output */
            .stSuccess {{
                background-color: rgba(0,0,0,0.9) !important;
                color: #00ffcc !important;
                border: 1px solid #00ffcc;
                border-radius: 12px;
                text-align: center;
                font-size: 18px;
                margin-top: 20px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception:
        pass


# Apply UI
apply_background_and_ui("earthquake_bg.jpg")

# =================================================
# LOAD MODEL PIPELINE
# =================================================
@st.cache_resource
def load_model():
    with open("eq_dt_pipeline_2.pkl", "rb") as f:
        return pickle.load(f)

pipeline = load_model()

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
# PREDICTION
# =================================================
if st.button("Predict Magnitude"):
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
    st.success(f"🌋 Predicted Earthquake Magnitude: **{prediction[0]:.2f}**")
