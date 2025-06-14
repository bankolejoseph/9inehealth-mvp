def get_emergency_data(patient_id: str):
    """
    Layer 1: Emergency access — no consent needed.
    Triggered via fingerprint match during field emergency.
    """
    return {
        "blood_type": "O+",
        "allergies": ["Penicillin"],
        "current_medications": ["Amoxicillin"],
        "chronic_conditions": ["Hypertension"]
    }

def get_full_history(patient_id: str, consent_token: str = None):
    """
    Layer 2: Full access — requires consent token (SMS, biometric unlock, etc.)
    """
    if not consent_token or consent_token != "VALID123":
        return {"error": "Access denied: patient consent not verified"}

    return {
        "lab_reports": ["CBC - May 2024", "ECG - Dec 2023"],
        "medical_notes": ["History of asthma", "Recent post-op recovery"],
        "vaccinations": ["COVID-19", "Tetanus", "Hepatitis B"]
    }
