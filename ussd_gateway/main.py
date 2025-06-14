from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from triage_model import triage
from dispatch import dispatch_ambulance
from blockchain_access import get_emergency_data, get_full_history
import psycopg2
import os

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
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ussd_logs (session_id, phone_number, text, priority, diagnosis, eta_minutes, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (session_id, phone, text, priority, diagnosis, eta, location))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"🛑 DB Logging Error: {e}")

@app.post("/ussd", response_class=PlainTextResponse)
async def ussd_handler(request: Request):
    form = await request.form()
    session_id = form.get("sessionId")
    phone = form.get("phoneNumber")
    text = form.get("text", "").strip()

    if text == "":
        return "CON Welcome to 9ineHealth Emergency Service.\n1. Heart Attack\n2. Bleeding\n3. Labour\n4. Fever"

    if "emergency info" in text.lower():
        data = get_emergency_data(phone)
        return f"END Blood Type: {data['blood_type']}, Allergies: {data['allergies']}"
    elif "full history" in text.lower():
        records = get_full_history(phone)
        return f"END Records: {', '.join(records)}"

    priority, diagnosis = triage(text)
    dispatch_info = dispatch_ambulance(priority, "Lagos")

    # 🔥 Log to DB
    log_request(session_id, phone, text, priority, diagnosis, dispatch_info["eta"], "Lagos")

    return f"END Triage result: {diagnosis} (Priority {priority}). Ambulance en route. ETA: {dispatch_info['eta']}."
