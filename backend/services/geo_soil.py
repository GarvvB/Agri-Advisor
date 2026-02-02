def estimate_soil_by_location(latitude, longitude):
    # Simple rule-based demo logic (research-backed concept)
    
    if 8 <= latitude <= 37:  # India tropical belt example
        soil_type = "Loamy"
        ph = 6.5
        nitrogen = 70
        phosphorus = 50
        potassium = 60
    elif latitude > 37:
        soil_type = "Clay"
        ph = 7.2
        nitrogen = 60
        phosphorus = 45
        potassium = 55
    else:
        soil_type = "Sandy"
        ph = 7.8
        nitrogen = 40
        phosphorus = 35
        potassium = 40

    return {
        "soil_type": soil_type,
        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium,
        "ph": ph
    }