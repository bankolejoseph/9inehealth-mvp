def dispatch_ambulance(priority_level: int, location: str):
    print(f"Dispatching ambulance to {location} with priority {priority_level}")
    return {
        "eta": "12 minutes",
        "co2_saved_kg": 6.3
    }
