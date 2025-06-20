def dispatch_ambulance(priority: int, location: str):
    """
    Mock dispatch logic.
    In production, integrate with GPS, traffic data, and ambulance availability.
    """
    eta = 12 if priority == 1 else 15
    return {
        "eta": eta,
        "location": location
    }
