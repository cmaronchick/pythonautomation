"""Configuration for the Bloodworks Northwest scraper."""

AO_ZIPCODES = {
    "Alpines": 98027,
    "Angmar": 98021,
    "Bloodsport": 98036,
    "Bobcat": 98052,
    "Bonsai": 98112,
    "Columbia City": 98118,
    "The Combine": 98117,
    "Counterbalance": 98118,
    "Doom": 98028,
    "Flash": 98115,
    "Gasworks": 98103,
    "Grasslawn": 98052,
    "Hawks Nest": 98043,
    "Heritage": 98033,
    "Hiawatha": 98116,
    "Hurricane Ridge": 98029,
    "KiMS": 98033,
    "Log Boom": 98028,
    "Mohai": 98109,
    "PBJ - City Hall": 98033,
    "PBJ - Doom": 98028,
    "PBJ - Google Monday": 98033,
    "PBJ - Google Thursday": 98033,
    "PBJ - Ravenna": 98105,
    "Perestroika": 98005,
    "Purple Haze": 98056,
    "Rat City": 98146,
    "Robinswood": 98007,
    "Ruck Mountain": 98033,
    "Sasquatch": 98034,
    "Soft Trot": 98028,
    "Space Needle": 98109,
    "Speakeasy": 98034,
    "Thunderdome": 98034,
    "Timber": 98072,
    "Torque": 98033,
    "Tundra": 98072,
    "Tundra Speed": 98072,
    "Valhalla": 98115
}

SEARCH_DAYS = 30
OUTPUT_DIR = "data"
SITE_DIR = "docs"
F3_API_URL = "https://api.f3nation.com/v1/location/in-bounding-box"
F3_BOUNDING_BOX = {
    "minLng": -122.474213,
    "minLat": 47.271986,
    "maxLng": -121.701050,
    "maxLat": 47.851010
}
