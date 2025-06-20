from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from triage_model import triage
from dispatch import dispatch_ambulance
from blockchain_access import get_emergency_data, get_full_history
import os
import psycopg2

app = FastAPI()

# DB config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "ninehealth")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "9inehealth_secure")

def log_request(session_id, phone, text, priority, diagnosis, eta, location):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ussd_logs (session_id, phone_number, text, priority, diagnosis, eta_minutes, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (session_id, phone, text, priority, diagnosis, eta, location))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Logging error:", e)

@app.post("/ussd", response_class=PlainTextResponse)
async def ussd_handler(request: Request):
    form = await request.form()
    session_id = form.get("sessionId")
    phone = form.get("phoneNumber")
    text = form.get("text", "").strip().lower()

    if text == "":
        return "CON Welcome to 9ineHealth Emergency Service.\n1. Heart Attack\n2. Bleeding\n3. Labour\n4. Fever"

    if "emergency" in text:
        data = get_emergency_data(phone)
        return f"END Blood Type: {data['blood_type']}, Allergies: {data['allergies']}"
    elif "full" in text:
        records = get_full_history(phone)
        return f"END Records: {records}"

    priority, diagnosis = triage(text)
    dispatch_info = dispatch_ambulance(priority, "Lagos")

    log_request(session_id, phone, text, priority, diagnosis, dispatch_info["eta"], "Lagos")

    return f"END Triage result: {diagnosis} (Priority {priority}). Ambulance en route. ETA: {dispatch_info['eta']}."

import uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
