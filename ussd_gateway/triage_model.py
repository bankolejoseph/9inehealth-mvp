import requests

def triage(symptom_text: str):
    try:
        response = requests.post(
            "https://trae-ai-mock-server.onrender.com/triage",  # Replace with TRAE live later
            json={"text": symptom_text},
            timeout=5
        )
        result = response.json()
        return result["priority"], result["diagnosis"]
    except Exception as e:
        print("TRAE fallback triggered:", str(e))
        text = symptom_text.lower()
        if "heart" in text:
            return 1, "Suspected cardiac issue"
        elif "bleeding" in text:
            return 2, "Active bleeding"
        elif "labour" in text:
            return 3, "Maternal emergency"
        elif "fever" in text:
            return 4, "Likely non-critical"
        else:
            return 5, "Unclassified / Telemedicine recommended"
