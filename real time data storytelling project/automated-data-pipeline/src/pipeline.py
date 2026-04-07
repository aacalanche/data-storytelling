import requests
import pandas as pd

BASE_URL = "https://www.freetogame.com/api"
TAGS = [
    "mmorpg", "shooter", "strategy", "moba", "racing", "sports", "social",
    "sandbox", "open-world", "survival", "pvp", "pve", "pixel", "voxel",
    "zombie", "turn-based", "first-person", "third-person", "top-down",
    "tank", "space", "sailing", "side-scroller", "superhero", "permadeath",
    "card", "battle-royale", "mmo", "mmofps", "mmotps", "3d", "2d", "anime",
    "fantasy", "sci-fi", "fighting", "action-rpg", "action", "military",
    "martial-arts", "flight", "low-spec", "tower-defense", "horror", "mmorts"
]
ORDERS = ["release-date", "popularity", "alphabetical", "relevance"]
PLATFORMS = ["windows", "browser", "all"]

def validate_params(params) -> bool:
    id = params.get("id")
    if id and len(params) > 1:
        return False

    for key, allowed in [("category", TAGS), ("sort-by", ORDERS), ("platform", PLATFORMS)]:
        value = params.get(key)
        if value and value not in allowed:
            return False
    
    return True

def fetch_games(params):
    if not validate_params(params):
        raise ValueError("Invalid parameters")
    id = params.get("id")
    endpoint = "game" if id else "games"

    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params, timeout=10)
    
    data = response.json()
    status = response.status_code
    response_url = response.url

    return {
        "data": data,
        "status": status,
        "url": response_url
    }

def parse_games(params):
    games = []

    result = fetch_games(params)
    data = result["data"]

    for game in data:
        record = {
            "id": game.get("id"),
            "title": game.get("title"),
            "genre": game.get("genre", "Unknown"),
            "platform": game.get("platform", "Unknown"),
            "publisher": game.get("publisher", "Unknown"),
            "release_date": game.get("release_date")
        }
        games.append(record)

    return games

def parse_category_list(categories, params):
    all_games = []

    for cat in categories:
        params["category"] = cat
        games = parse_games(params)
        all_games.extend(games)

    return all_games


def main():
    params = {"category": ["shooter", "sci-fi"], "platform": "windows", "sort-by": "alphabetical"}

    platform = params.get("platform")
    if isinstance(platform, list):
        params["platform"] = "all" if len(platform) > 1 else platform[0]

    categories = params.get("category")
    if categories and isinstance(categories, list) and len(categories) > 1:
        games = parse_category_list(categories, params)
    else:
        games = parse_games(params)
    
    df_games = pd.DataFrame(games)
    print(df_games.head(10))

if __name__ == "__main__":
    main()