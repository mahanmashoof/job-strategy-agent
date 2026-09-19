"""Centralized geographic filtering for remote job listings."""

# ISO alpha-2 codes for EU countries + Brazil
EU_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
    "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
    "PL", "PT", "RO", "SK", "SI", "ES", "SE"
}
BRAZIL = {"BR"}
TARGET_COUNTRIES = EU_COUNTRIES | BRAZIL

# Strings that indicate "worldwide" / "anywhere"
WORLDWIDE_STRINGS = [
    "worldwide", "anywhere", "global", "remote", "any location",
    "no restriction", "international"
]

# Region strings that map to multiple countries
REGION_ALIASES = {
    "europe": EU_COUNTRIES,
    "eu": EU_COUNTRIES,
    "emea": EU_COUNTRIES | {"BR"},
}


def is_target_location(location_raw: str, location_restrictions: list = None) -> tuple[bool, str]:
    """
    Determine if a job's location matches our target (EU + Brazil + Worldwide).
    
    Returns: (passes_filter: bool, reason: str)
    """
    # Prefer structured locationRestrictions if available (Himalayas)
    if location_restrictions:
        codes = set()
        for r in location_restrictions:
            if isinstance(r, dict):
                code = r.get("alpha2", "").upper()
            elif isinstance(r, str):
                code = r.upper()
            else:
                continue
            if code:
                codes.add(code)
        
        if not codes:
            return True, "no restrictions (worldwide)"
        
        if codes & TARGET_COUNTRIES:
            return True, f"matches target: {codes & TARGET_COUNTRIES}"
        
        # Check for region aliases in the raw names
        for r in location_restrictions:
            if isinstance(r, dict):
                name = r.get("name", "").lower()
                for alias, countries in REGION_ALIASES.items():
                    if alias in name:
                        return True, f"region alias: {alias}"
        
        return False, f"restricted to: {codes}"
    
    # Fall back to string parsing
    if not location_raw:
        return True, "no location specified"
    
    text = location_raw.lower().strip()
    
    # Worldwide indicators
    for indicator in WORLDWIDE_STRINGS:
        if indicator in text:
            return True, f"worldwide indicator: {indicator}"
    
    # Brazil
    if "brazil" in text or "brasil" in text or "br" == text:
        return True, "brazil"
    
    # EU country names
    eu_names = [
        "germany", "france", "spain", "italy", "netherlands", "poland",
        "sweden", "denmark", "finland", "ireland", "portugal", "austria",
        "belgium", "czech", "romania", "greece", "hungary", "bulgaria",
        "croatia", "estonia", "latvia", "lithuania", "luxembourg",
        "malta", "slovakia", "slovenia", "cyprus"
    ]
    for name in eu_names:
        if name in text:
            return True, f"eu country: {name}"
    
    # Region indicators
    if "europe" in text or "eu " in text or text.startswith("eu"):
        return True, "europe region"
    
    # If it mentions a specific non-target country, reject
    non_target_indicators = [
        "usa", "united states", "us only", "canada", "uk only", "united kingdom",
        "asia", "india", "australia", "japan", "singapore", "china"
    ]
    for indicator in non_target_indicators:
        if indicator in text:
            # But if it ALSO has a target country, pass
            return False, f"non-target: {indicator}"
    
    # Unknown locations — pass by default (better to over-include than miss)
    return True, f"unknown location, passing: {text[:50]}"