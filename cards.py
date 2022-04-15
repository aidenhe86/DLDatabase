import requests

API_BASE_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php?format=Duel%20Links"

def request_card(card):
    """return cards information base on given endpoint"""
    
    url = API_BASE_URL

    # All card
    if "name" in card:
        name = card["name"]
        url = f"{url}&fname={name}"

    if "type" in card:
        t = card["type"]
        url = f"{url}&type={t}"
    
    if "race" in card:
        r = card["race"]
        url = f"{url}&race={r}"
    
    # Monster
    if "attribute" in card:
        a = card["attribute"]
        url = f"{url}&attribute={a}"
    
    if "atk" in card:
        a = card["atk"]
        url = f"{url}&atk={a}"

    if "def" in card:
        d = card["def"]
        url = f"{url}&def={d}"

    if "level" in card:
        l = card["level"]
        url = f"{url}&level={l}"

    if "scale" in card:
        s = card["scale"]
        url = f"{url}&scale={s}"
    
    # return error if error already found
    if "error" in card:
        return card["error"]

    # send API request
    response = requests.get(url)
    r = response.json()

    # If API returns a error
    if r.get("error"):
        return {"error": "No card matching! Please try again."}

    else:
        cards = r["data"][:10]
        return cards
