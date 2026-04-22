from django.contrib import admin
from .models import Game, Genre, Publisher

class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'publisher', 'platform')
    list_filter = ('genre', 'publisher', 'platform')
    search_fields = ('title', 'publisher__name')

admin.site.register(Game, GameAdmin)
admin.site.register(Genre)
admin.site.register(Publisher)

