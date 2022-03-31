import requests

API_BASE_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php?format=Duel%20Links"

def request_card_name(name):
    """return cards information by searching the given name"""
    url = f"{API_BASE_URL}&fname={name}"
    response = requests.get(url)
    r = response.json()
    if not name or r.get("error"):
        return []
    else:
        cards = r["data"][:10]
        return cards
