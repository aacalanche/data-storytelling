import requests
import pandas as pd
import sqlite3
from pathlib import Path

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
DATA_DIR = Path("../data/processed")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def validate_params(params) -> bool:
    id = params.get("id")
    if id and len(params) > 1:
        return False

    validations = [
        ("category", TAGS),
        ("sort-by", ORDERS),
        ("platform", PLATFORMS)
    ]
    for key, allowed in validations:
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

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "data": data,
            "status": response.status_code,
            "url": response.url
        }

    except requests.exceptions.Timeout:
        print("The request timed out.")
        return {
            "data": [],
            "status": None,
            "url": url
        }

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        return {
            "data": [],
            "status": None,
            "url": url
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


def load_to_sqlite(df: pd.DataFrame) -> None:
    db_path = DATA_DIR / "games.db"
    conn = sqlite3.connect(db_path)

    df = df.drop_duplicates(subset=["id"])

    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name='games'"
    )
    table_exists = cursor.fetchone()

    if table_exists:
        query = "SELECT id FROM games"
        existing_ids = pd.read_sql_query(query, conn)['id'].tolist()
        df = df[~df['id'].isin(existing_ids)]

    if not df.empty:
        df.to_sql("games", conn, if_exists="append", index=False)

    report = pd.read_sql("SELECT COUNT(*) AS total_records FROM games", conn)
    print(report)

    conn.close()


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
    df_games = df_games.drop_duplicates(subset=["id"])
    print(df_games.head(10))

    load_to_sqlite(df_games)


if __name__ == "__main__":
    main()
