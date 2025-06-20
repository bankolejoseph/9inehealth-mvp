def dispatch_ambulance(priority: int):
    location = "Lagos"
    eta = 10 if priority == 1 else 15
    return {
        "location": location,
        "eta": eta
    }
