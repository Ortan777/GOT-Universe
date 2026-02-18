def format_got_date(date_string):
    """
    Format Game of Thrones dates properly.
    Handles formats like: "81 AC", "27 BC", "130 AC", etc.
    """
    if not date_string:
        return "Unknown"
    
    date_string = str(date_string).strip()
    
    # Remove any duplicate AC/BC
    if "AC AC" in date_string:
        date_string = date_string.replace("AC AC", "AC")
    if "BC BC" in date_string:
        date_string = date_string.replace("BC BC", "BC")
    if "AC BC" in date_string or "BC AC" in date_string:
        # This is invalid, take the first one
        parts = date_string.split()
        if len(parts) >= 2:
            date_string = f"{parts[0]} {parts[1]}"
    
    # Ensure proper spacing
    if "AC" in date_string and "AC" not in date_string.split()[-1]:
        date_string = date_string.replace("AC", " AC").strip()
    if "BC" in date_string and "BC" not in date_string.split()[-1]:
        date_string = date_string.replace("BC", " BC").strip()
    
    # Handle numeric only (assume AC)
    if date_string.isdigit():
        return f"{date_string} AC"
    
    return date_string

def get_character_era_description(born, died):
    """Get a descriptive era for a character"""
    born_formatted = format_got_date(born)
    died_formatted = format_got_date(died)
    
    if "BC" in born_formatted and "AC" in died_formatted:
        return "Lived through the Conquest"
    elif "BC" in born_formatted:
        return "Born before the Conquest"
    elif "AC" in born_formatted and int(born_formatted.split()[0]) < 100:
        return "Early Targaryen era"
    elif "AC" in born_formatted and int(born_formatted.split()[0]) > 250:
        return "Pre-Robert's Rebellion era"
    else:
        return ""