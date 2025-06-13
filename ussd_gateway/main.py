from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from triage_model import triage
from dispatch import dispatch_ambulance

app = FastAPI()

@app.post("/ussd", response_class=PlainTextResponse)
async def ussd_handler(request: Request):
    form = await request.form()
    session_id = form.get("sessionId")
    phone = form.get("phoneNumber")
    text = form.get("text", "").strip()

    print(f"📞 Incoming USSD: session={session_id}, phone={phone}, text={text}")

    if text == "":
        return "CON Welcome to 9ineHealth Emergency Service.\n1. Heart Attack\n2. Bleeding\n3. Labour\n4. Fever"

    priority, diagnosis = triage(text)
    dispatch_info = dispatch_ambulance(priority, "Lagos")

    return f"END Triage result: {diagnosis} (Priority {priority}). Ambulance en route. ETA: {dispatch_info['eta']}."
