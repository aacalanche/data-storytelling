import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from games.models import Game, Genre, Publisher

BASE_URL = "https://www.freetogame.com/api/games"
TAGS = [
    "mmorpg", "shooter", "strategy", "moba", "racing", "sports", "social",
    "sandbox", "open-world", "survival", "pvp", "pve", "pixel", "voxel",
    "zombie", "turn-based", "first-person", "third-person", "top-down",
    "tank", "space", "sailing", "side-scroller", "superhero", "permadeath",
    "card", "battle-royale", "mmo", "mmofps", "mmotps", "3d", "2d", "anime",
    "fantasy", "sci-fi", "fighting", "action-rpg", "action", "military",
    "martial-arts", "flight", "low-spec", "tower-defense", "horror", "mmorts"
]

class Command(BaseCommand):
    help = 'Fetch latest game data from Games API'

    def handle(self, *args, **options):
        total_saved = 0
        for tag in TAGS:
            try:
                resp = requests.get(BASE_URL,
                    params={'category': tag, "platform": "all",
                            },
                    timeout=10
                    )
                resp.raise_for_status()
                data = resp.json()

                with transaction.atomic():
                    for item in data:
                        genre, _ = Genre.objects.get_or_create(
                            name=item.get("genre") or "Unknown"
                        )
                        publisher, _ = Publisher.objects.get_or_create(
                            name=item.get("publisher") or "Unknown"
                        )
                        Game.objects.update_or_create(
                            api_id=item.get("id"),
                            defaults={
                                "genre": genre,
                                "publisher": publisher,
                                "platform": item.get("platform") or "Unknown",
                                "title": item.get("title") or "Unknown",
                                "release_date": item.get("release_date") or "Unknown",
                                "developer": item.get("developer"),
                                "source": "api",
                            }
                        )
                        total_saved += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Fetched {len(data)} times from: {tag}"
                    )
                )
            except requests.exceptions.RequestException as e:
                self.stderr.write(
                    self.style.ERROR(
                        f"Error fetching {tag} from API: {e}"
                    )
                )
        self.stdout.write(self.style.SUCCESS(
            f"Fetched {total_saved} times"
        ))

