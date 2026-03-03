import math


# -----------------------------
# Drywall
# -----------------------------
def calculate_drywall(area_sqft: float, price_per_sheet: float = 15.0):
    sheets = math.ceil(area_sqft / 32)
    total_cost = sheets * price_per_sheet

    return {
        "sheets_needed": sheets,
        "estimated_cost": round(total_cost, 2)
    }


# -----------------------------
# Concrete
# -----------------------------
def calculate_concrete(volume_cubic_feet: float, price_per_yard: float = 180.0):
    yards = volume_cubic_feet / 27
    total_cost = yards * price_per_yard

    return {
        "cubic_yards": round(yards, 2),
        "estimated_cost": round(total_cost, 2)
    }


# -----------------------------
# Stairs
# -----------------------------
def calculate_stairs(total_height_inches: float):
    riser_height = 7.0  # standard
    risers = math.ceil(total_height_inches / riser_height)
    actual_riser_height = total_height_inches / risers

    return {
        "riser_count": risers,
        "riser_height_inches": round(actual_riser_height, 2)
    }


# -----------------------------
# Paint
# -----------------------------
def calculate_paint(area_sqft: float, price_per_gallon: float = 45.0):
    gallons = math.ceil(area_sqft / 350)
    total_cost = gallons * price_per_gallon

    return {
        "gallons_needed": gallons,
        "estimated_cost": round(total_cost, 2)
    }
