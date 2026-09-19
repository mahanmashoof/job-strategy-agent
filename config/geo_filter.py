"""Centralized geographic filtering for remote job listings."""

EU_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
    "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
    "PL", "PT", "RO", "SK", "SI", "ES", "SE"
}
BRAZIL = {"BR"}
TARGET_COUNTRIES = EU_COUNTRIES | BRAZIL

WORLDWIDE_STRINGS = [
    "worldwide", "anywhere", "global", "any location",
    "no restriction", "international", "remote"
]

EU_NAMES = [
    "germany", "france", "spain", "italy", "netherlands", "poland",
    "sweden", "denmark", "finland", "ireland", "portugal", "austria",
    "belgium", "czech", "romania", "greece", "hungary", "bulgaria",
    "croatia", "estonia", "latvia", "lithuania", "luxembourg",
    "malta", "slovakia", "slovenia", "cyprus"
]

NON_TARGET = [
    "united states", "usa", "canada", "united kingdom", "uk only",
    "asia", "india", "australia", "japan", "singapore", "china",
    "philippines", "pakistan", "nigeria", "kenya", "mexico"
]


def is_target_location(location_raw: str, location_restrictions: list = None) -> tuple[bool, str]:
    """Returns (passes_filter, reason)"""
    
    # Structured restrictions (Himalayas)
    if location_restrictions:
        codes = set()
        names_lower = []
        for r in location_restrictions:
            if isinstance(r, dict):
                code = r.get("alpha2", "").upper()
                name = r.get("name", "").lower()
                if code:
                    codes.add(code)
                if name:
                    names_lower.append(name)
            elif isinstance(r, str):
                codes.add(r.upper())
                names_lower.append(r.lower())
        
        if not codes and not names_lower:
            return True, "no restrictions"
        
        if codes & TARGET_COUNTRIES:
            return True, f"target code: {codes & TARGET_COUNTRIES}"
        
        # Check names for EU countries
        for name in names_lower:
            if any(eu in name for eu in EU_NAMES):
                return True, f"EU name: {name}"
            if "brazil" in name or "brasil" in name:
                return True, "brazil"
        
        return False, f"restricted: {codes or names_lower}"
    
    # String fallback
    if not location_raw:
        return True, "no location"
    
    text = location_raw.lower().strip()
    
    for ind in WORLDWIDE_STRINGS:
        if ind in text:
            return True, f"worldwide: {ind}"
    
    if "brazil" in text or "brasil" in text:
        return True, "brazil"
    
    for name in EU_NAMES:
        if name in text:
            return True, f"EU: {name}"
    
    for ind in NON_TARGET:
        if ind in text:
            return False, f"non-target: {ind}"
    
    return True, f"unknown, passing"