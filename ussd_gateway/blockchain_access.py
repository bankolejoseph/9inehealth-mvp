def get_emergency_data(patient_id: str):
    return {
        "blood_type": "O+",
        "allergies": ["penicillin"],
        "current_medications": ["amoxicillin"],
        "chronic_conditions": ["hypertension"]
    }

def get_full_history(patient_id: str, consent_token: str):
    return {
        "lab_reports": ["CBC (2024)", "ECG (2023)"],
        "medical_notes": ["Post-op review", "Family history of stroke"],
        "vaccinations": ["COVID-19", "Tetanus"]
    }
