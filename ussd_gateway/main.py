from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from triage_model import triage
from dispatch import dispatch_ambulance
from blockchain_access import get_emergency_data, get_full_history  # ✅ Moved up

import uvicorn

app = FastAPI()

@app.post("/ussd", response_class=PlainTextResponse)
async def ussd_handler(request: Request):
    form = await request.form()
    session_id = form.get("sessionId")
    phone = form.get("phoneNumber")
    text = form.get("text", "").strip()

    print(f"📞 Incoming USSD: session={session_id}, phone={phone}, text={text}")

    # Menu
    if text == "":
        return "CON Welcome to 9ineHealth Emergency Service.\n1. Heart Attack\n2. Bleeding\n3. Labour\n4. Fever"

    # Layer 1: Emergency record access
    if text.lower() == "get emergency info":
        patient_data = get_emergency_data("user-123")
        return f"END Blood Type: {patient_data['blood_type']}, Allergies: {', '.join(patient_data['allergies'])}"

    # Layer 2: Full history with consent
    if text.lower() == "get full history":
        history = get_full_history("user-123", consent_token="VALID123")
        if "error" in history:
            return f"END {history['error']}"
        return f"END Records: {', '.join(history['lab_reports'])}"

    # Standard triage
    priority, diagnosis = triage(text)
    dispatch_info = dispatch_ambulance(priority, "Lagos")

    return f"END Triage result: {diagnosis} (Priority {priority}). Ambulance en route. ETA: {dispatch_info['eta']}."


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
