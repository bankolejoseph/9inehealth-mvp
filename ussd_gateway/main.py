from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()

@app.post("/ussd", response_class=PlainTextResponse)
async def ussd_handler(request: Request):
    form = await request.form()
    session_id = form.get("sessionId", "")
    phone_number = form.get("phoneNumber", "")
    text = form.get("text", "")

    if text == "":
        response = "CON Welcome to 9ineHealth Emergency Service.\n1. Heart Attack\n2. Bleeding\n3. Labour\n4. Fever"
    elif text == "1":
        response = "END Emergency for suspected cardiac issue logged. Help is on the way."
    elif text == "2":
        response = "END Bleeding emergency logged. Ambulance dispatched."
    elif text == "3":
        response = "END Labour emergency recorded. Stay calm. Help is near."
    elif text == "4":
        response = "END Non-critical symptoms received. A remote doctor will contact you."
    else:
        response = "END Invalid option. Please dial again."

    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
