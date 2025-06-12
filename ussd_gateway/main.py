from fastapi import FastAPI, Request
from pydantic import BaseModel
from triage_model import predict_priority
from blockchain_access import fetch_emergency_record

app = FastAPI()

class USSDInput(BaseModel):
    sessionId: str
    phoneNumber: str
    text: str  # This represents the symptom or situation description

@app.post("/ussd")
async def handle_ussd(data: USSDInput):
    triage_level, condition = predict_priority(data.text)
    patient_data = fetch_emergency_record(data.phoneNumber)

    response = {
        "triage_level": triage_level,
        "condition": condition,
        "record": patient_data,
    }
    return response

@app.get("/")
async def root():
    return {"message": "9ineHealth USSD Gateway is live"}
