def traffic_decision(plates):
    count = len(plates)
    if count >= 8:
        level, recommendation = "HIGH", "Consider diversion / alternate route"
    elif count >= 4:
        level, recommendation = "MEDIUM", "Monitor traffic"
    else:
        level, recommendation = "LOW", "Normal flow"
    return {
        "vehicle_count": count,
        "unique_plates": len(set(p["text"] for p in plates if p["text"])),
        "traffic_level": level,
        "recommendation": recommendation,
    }
