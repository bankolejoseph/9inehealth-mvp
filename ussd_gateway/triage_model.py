def predict_priority(symptom_text):
    """
    Mock triage function. In production, replace with TRAE AI or Vertex AI model call.
    """
    text = symptom_text.lower()

    if "chest pain" in text or "heart" in text:
        return 1, "Suspected cardiac issue"
    elif "bleeding" in text or "cut" in text:
        return 2, "Active bleeding"
    elif "labour" in text or "baby" in text:
        return 3, "Maternal emergency"
    elif "fever" in text or "headache" in text:
        return 4, "Likely non-critical"
    else:
        return 5, "Unclassified / Telemedicine recommended"
