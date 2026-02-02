from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import requests

from services.geo_soil import estimate_soil_by_location
from services.weather_service import get_weather
from services.labor_service import estimate_labor
from simulation.farm_simulator import FarmSimulator


# ================= CREATE APP FIRST =================
app = FastAPI(title="Agri-Advisor API")

# ================= ENABLE CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= LOAD ML MODELS =================
crop_model = joblib.load("crop_model.pkl")
crop_encoder = joblib.load("crop_encoder.pkl")

# ================= ROOT =================
@app.get("/")
def home():
    return {"message": "Agri-Advisor Backend Running"}

# ================= SOIL SIMULATION DEMO =================
@app.get("/simulate-day")
def simulate_day(temp: float = 30, humidity: float = 70, rain: float = 0):
    simulator = FarmSimulator(70, 50, 60, 6.5)
    data = simulator.simulate_day(temp, humidity, rain)
    return {"simulated_data": data}

# ================= DIRECT CROP PREDICTION =================
@app.get("/predict-crop")
def predict_crop(n: float, p: float, k: float, temp: float, humidity: float, ph: float, rain: float):
    features = np.array([[n, p, k, temp, humidity, ph, rain]])
    prediction_encoded = crop_model.predict(features)
    prediction = crop_encoder.inverse_transform(prediction_encoded)
    return {"recommended_crop": prediction[0]}

# ================= FULL AI ADVISORY SYSTEM =================
@app.get("/full-advisory")
def full_advisory(lat: float, lon: float, area: float, workers: int):

    soil = estimate_soil_by_location(lat, lon)
    weather = get_weather(lat, lon)

    simulator = FarmSimulator(
        soil["nitrogen"],
        soil["phosphorus"],
        soil["potassium"],
        soil["ph"]
    )

    sim_data = simulator.simulate_day(
        weather["temperature"],
        weather["humidity"],
        weather["rainfall"]
    )

    features = np.array([[sim_data["nitrogen"], sim_data["phosphorus"], sim_data["potassium"],
                          weather["temperature"], weather["humidity"], sim_data["ph"], weather["rainfall"]]])

    crop_encoded = crop_model.predict(features)
    crop = crop_encoder.inverse_transform(crop_encoded)[0]

    labor = estimate_labor(crop, area, workers)

    return {
        "location_soil_estimate": soil,
        "weather": weather,
        "simulated_soil": sim_data,
        "recommended_crop": crop,
        "labor_plan": labor
    }

# ================= AI ASSISTANT (REAL LLM) =================
OPENROUTER_API_KEY = "API_KEY"

@app.post("/ai-assistant")
def ai_assistant(question: str = Body(..., embed=False)):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are Agri-Advisor, an AI agronomist helping farmers."},
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    reply = response.json()["choices"][0]["message"]["content"]

    return {"response": reply}

# ================= MODEL PERFORMANCE =================
@app.get("/model-stats")
def model_stats():
    return {
        "accuracy": 0.993,
        "precision": 0.99,
        "recall": 0.99,
        "f1": 0.99
    }


