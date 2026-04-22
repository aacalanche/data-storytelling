from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    api_id = models.IntegerField(unique=True, null=True, blank=True)

    title = models.CharField(max_length=400)

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    platform = models.CharField(max_length=200, blank=True, default="Unknown")
    release_date = models.DateField(null=True, blank=True)
    developer = models.CharField(max_length=200, blank=True, default="Unknown")

    na_sales = models.FloatField(null=True, blank=True)
    eu_sales = models.FloatField(null=True, blank=True)
    jp_sales = models.FloatField(null=True, blank=True)
    other_sales = models.FloatField(null=True, blank=True)
    global_sales = models.FloatField(null=True, blank=True)

    critic_score = models.FloatField(null=True, blank=True)
    critic_count = models.IntegerField(null=True, blank=True)
    user_score = models.FloatField(null=True, blank=True)
    user_count = models.IntegerField(null=True, blank=True)

    rating = models.CharField(max_length=50,
        choices =[("AO", "AO"), ("M", "M"), ("E", "E"),
                  ("T", "T"), ("E10+", "E10+"), ("EC", "EC"),
                  ("Unknown", "Unknown"),], blank=True, default="Unknown")
    source = models.CharField(max_length=50,
        choices=[("csv", "CSV Import"),("api", "API Fetch"),], default="csv")

    def __str__(self):
        return self.title
