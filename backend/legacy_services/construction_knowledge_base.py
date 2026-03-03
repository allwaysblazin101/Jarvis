CONSTRUCTION_RULES = {

    "stairs_comfort_formula": {
        "formula": "2R + T = 24 inches",
        "description": "Standard stair comfort formula"
    },

    "drywall_coverage": {
        "formula": "1 sheet = 32 sq ft",
        "description": "Standard 4x8 drywall sheet"
    },

    "concrete_conversion": {
        "formula": "1 cubic yard = 27 cubic feet",
        "description": "Concrete yard conversion"
    },

    "paint_coverage": {
        "formula": "1 gallon = 350 sq ft",
        "description": "Average interior paint coverage"
    }
}


def get_construction_rule(key: str):
    return CONSTRUCTION_RULES.get(key)
