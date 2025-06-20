def triage(text):
    try:
        if "bleeding" in text.lower():
            return {
                "diagnosis": "Active bleeding",
                "priority": 2
            }
        elif "heart" in text.lower():
            return {
                "diagnosis": "Suspected cardiac issue",
                "priority": 1
            }
        else:
            return {
                "diagnosis": "Non-critical condition",
                "priority": 3
            }
    except Exception as e:
        print(f"Error during triage: {e}")
        return {
            "diagnosis": "Unknown error during triage",
            "priority": 3
        }
