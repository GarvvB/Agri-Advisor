def estimate_labor(crop, area_acres, workers_available):
    labor_hours_per_acre = {
        "rice": 18,
        "wheat": 10,
        "maize": 7,
        "cotton": 12,
        "sugarcane": 15
    }

    hours_needed = labor_hours_per_acre.get(crop.lower(), 8) * area_acres
    hours_available = workers_available * 8 * 6  # 6 days/week

    return {
        "hours_needed_per_week": hours_needed,
        "hours_available_per_week": hours_available,
        "labor_sufficient": hours_available >= hours_needed
    }