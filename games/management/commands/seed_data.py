from django.core.management.base import BaseCommand
from games.models import Game, Genre, Publisher
import csv
from datetime import datetime

class Command(BaseCommand):
    help = "load CSV game data"

    def handle(self, *args, **kwargs):
        with open("data/processed/videogamesales_clean.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                genre_name = row["Genre"]
                publisher_name = row["Publisher"]

                genre_obj, created = Genre.objects.get_or_create(name=genre_name)
                publisher_obj, created = Publisher.objects.get_or_create(name=publisher_name)

                Game.objects.get_or_create(
                    title=row["Name"],
                    genre=genre_obj,
                    publisher=publisher_obj,
                    platform=row["Platform"],
                    release_date=row["Year_of_Release"],
                    developer=row["Developer"],
                    rating=row["Rating"],
                    source="csv",
                    na_sales=row["NA_Sales"] or None,
                    eu_sales=row["EU_Sales"] or None,
                    jp_sales=row["JP_Sales"] or None,
                    other_sales=row["Other_Sales"] or None,
                    global_sales=row["Global_Sales"] or None,
                    critic_score=row["Critic_Score"] or None,
                    critic_count=row["Critic_Count"] or None,
                    user_score=row["User_Score"] or None,
                    user_count=row["User_Count"] or None,
                )

        self.stdout.write("Data loaded")