from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Game


def home(request):
    return render(request, "games/home.html")


def form(request):
    return render(request, "games/form.html")


def analytics(request):
    return render(request, "games/analytics.html")


def confirm_delete(request):
    return render(request, "games/confirm_delete.html")


class GameListView(ListView):
    model = Game
    template_name = "games/list.html"
    context_object_name = "games"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.path == '/games/complete/':
            return queryset.filter(is_done=True)
        return queryset
    

class GameDetailView(DetailView):
    model = Game
    template_name = "games/game_detail.html"
    context_object_name = "game"
