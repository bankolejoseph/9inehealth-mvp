def fetch_emergency_record(identifier):
    """
    Mock function to simulate biometric lookup (e.g., fingerprint or phone number).
    Returns Layer 1 medical data only (emergency-relevant).
    """

    fake_db = {
        "08012345678": {
            "blood_type": "O+",
            "allergies": ["Penicillin"],
            "medications": ["Lisinopril"],
            "last_updated": "2025-06-01"
        },
        "08098765432": {
            "blood_type": "A-",
            "allergies": [],
            "medications": ["Metformin"],
            "last_updated": "2025-05-28"
        }
    }

    return fake_db.get(identifier, {
        "blood_type": "Unknown",
        "allergies": [],
        "medications": [],
        "last_updated": "Unknown"
    })
