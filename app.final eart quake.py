import streamlit as st
import pickle
import pandas as pd
import base64

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Earthquake Magnitude Prediction",
    layout="centered"
)

# -------------------------------------------------
# Convert JPG background image to base64
# -------------------------------------------------
def get_base64_bg(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_image = get_base64_bg("earthquake_bg.jpg")

# -------------------------------------------------
# Apply Background Image
# -------------------------------------------------
st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpeg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    color: white;
}}

/* Dark overlay for readability */
.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
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

/* Inputs */
input {{
    background-color: rgba(0,0,0,0.75) !important;
    color: white !important;
    border: 1px solid #00ffcc !important;
    border-radius: 8px !important;
}}

/* Increment / Decrement buttons */
button[title="Increment"],
button[title="Decrement"] {{
    background-color: #222 !important;
    color: white !important;
}}

/* Predict button */
.stButton > button {{
    width: 100%;
    background-color: #00ffcc;
    color: black;
    font-weight: bold;
    border-radius: 10px;
    padding: 0.7em;
    border: none;
    margin-top: 15px;
}}

/* Prediction output */
.stSuccess {{
    background-color: rgba(0,0,0,0.85) !important;
    color: #00ffcc !important;
    border: 1px solid #00ffcc;
    border-radius: 10px;
    text-align: center;
    font-size: 18px;
}}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Load Model (UNCHANGED)
# -------------------------------------------------
with open("eq_dt_pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("🌍 Earthquake Magnitude Prediction")

# -------------------------------------------------
# Inputs (UNCHANGED — exact training order)
# -------------------------------------------------
latitude = st.number_input("Latitude", value=0.0)
longitude = st.number_input("Longitude", value=0.0)
depth = st.number_input("Depth (km)", value=0.0)
dmin = st.number_input("Dmin", value=0.0)
rms = st.number_input("RMS", value=0.0)
horizontalError = st.number_input("Horizontal Error", value=0.0)
depthError = st.number_input("Depth Error", value=0.0)

# -------------------------------------------------
# Prediction (UNCHANGED)
# -------------------------------------------------
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



