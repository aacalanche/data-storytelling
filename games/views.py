from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.views.decorators.http import require_POST
from .models import Game, Genre, Publisher
from .forms import GameForm


@staff_member_required
@require_POST
def fetch_data_view(request):
    call_command("fetch_data")
    return redirect("game_list")


def home(request):
    return render(request, "games/home.html")


class GameListView(ListView):
    model = Game
    template_name = "games/game_list.html"
    context_object_name = "games"
    paginate_by = 20
    

class GameDetailView(DetailView):
    model = Game
    template_name = "games/game_detail.html"
    context_object_name = "game"


class GameCreateView(CreateView):
    model = Game
    form_class = GameForm
    template_name = "games/game_form.html"
    success_url = reverse_lazy('game_list')


class GameUpdateView(UpdateView):
    model = Game
    form_class = GameForm
    template_name = "games/game_form.html"
    
    def get_success_url(self):
        return reverse_lazy('game_detail', kwargs={'pk': self.object.pk})


class GameDeleteView(DeleteView):
    model = Game
    template_name = "games/game_confirm_delete.html"
    success_url = reverse_lazy('game_list')


def analytics(request):
    # Placeholder for analytics view - can be expanded with actual analytics logic
    
    return render(request, "games/analytics.html")