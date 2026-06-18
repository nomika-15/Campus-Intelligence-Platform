from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

# Load model
model = joblib.load("../models/placement_model.pkl")


@app.get("/")
def home():
    return {
        "message": "Campus Intelligence Platform API is running"
    }


@app.get("/predict")
def predict(
    cgpa: float,
    attendance: int,
    coding_score: int,
    aptitude_score: int,
    communication_score: int,
    projects_count: int,
    internships_count: int,
    hackathon_count: int
):

    student = np.array([[
        cgpa,
        attendance,
        coding_score,
        aptitude_score,
        communication_score,
        projects_count,
        internships_count,
        hackathon_count
    ]])

    prediction = model.predict(student)[0]
    probability = model.predict_proba(student)[0][1]

    return {
        "prediction": "Likely Placed" if prediction == 1 else "Not Likely Placed",
        "placement_probability": round(probability * 100, 2)
    }
