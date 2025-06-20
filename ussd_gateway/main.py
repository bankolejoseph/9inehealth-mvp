from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
import os
import psycopg2
import traceback
from triage_model import triage
from dispatch import dispatch_ambulance

app = FastAPI()

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# DB logging function
def log_to_db(data):
    try:
        print("📥 Connecting to DB...")
        print(f"🛠 Host={DB_HOST}, DB={DB_NAME}, User={DB_USER}")

        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )

        cur = conn.cursor()
        print("📤 Inserting data:", data)

        cur.execute("""
            INSERT INTO ussd_logs (session_id, phone_number, text, priority, diagnosis, eta_minutes, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data["session_id"],
            data["phone_number"],
            data["text"],
            data["priority"],
            data["diagnosis"],
            data["eta_minutes"],
            data["location"]
        ))

        conn.commit()
        cur.close()
        conn.close()
        print("✅ DB Logging Success!")

    except Exception as e:
        print(f"🛑 DB Logging Error: {e}")
        traceback.print_exc()

@app.post("/ussd", response_class=PlainTextResponse)
async def ussd_handler(
    sessionId: str = Form(...),
    phoneNumber: str = Form(...),
    text: str = Form(...)
):
    print(f"📞 Incoming USSD: session={sessionId}, phone= {phoneNumber}, text={text}")

    try:
        # Step 1: Perform triage
        triage_result = triage(text)

        # Step 2: Dispatch ambulance
        dispatch_info = dispatch_ambulance(triage_result["priority"])

        # Step 3: Log to DB
        log_data = {
            "session_id": sessionId,
            "phone_number": phoneNumber,
            "text": text,
            "priority": triage_result.get("priority"),
            "diagnosis": triage_result.get("diagnosis"),
            "eta_minutes": dispatch_info.get("eta"),
            "location": dispatch_info.get("location")
        }
        log_to_db(log_data)

        # Step 4: Respond to USSD request
        response = f"END Triage result: {triage_result['diagnosis']} (Priority {triage_result['priority']}). "
        response += f"Ambulance en route. ETA: {dispatch_info['eta']}."
        return response

    except Exception as e:
        print(f"🛑 Error: {e}")
        traceback.print_exc()
        return "END Sorry, an error occurred while processing your request."
