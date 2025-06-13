import requests

def triage(symptom_text: str):
    """
    Connects to TRAE AI for emergency triage. Replace mock if endpoint is ready.
    """
    try:
        response = requests.post(
            "https://trae-ai-endpoint.ngrok.io/predict",  # Replace with actual TRAE endpoint
            json={"text": symptom_text},
            timeout=5
        )
        result = response.json()
        return result["priority"], result["diagnosis"]
    except Exception:
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
