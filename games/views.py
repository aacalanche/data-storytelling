from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Game, Genre, Publisher
from .forms import GameForm
import json
import pandas as pd


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
    qs = Game.objects.all().values(
        'title',
        'platform',
        'genre',
        'publisher',
        'rating',
        'na_sales',
        'eu_sales',
        'jp_sales',
        'other_sales',
        'global_sales',
        'critic_score',
        'user_score',
    )

    df = pd.DataFrame(list(qs))

    if df.empty:
        return render(request, 'games/analytics.html', {
            'total_games': 0,
            'total_global_sales': 0,
            'avg_critic_score': 0,
            'avg_user_score': 0,
            'top_games': [],
            'sales_by_genre': [],
            'sales_by_platform': [],
            'top_publishers': [],
            'regional_sales': {
                'na_sales': 0,
                'eu_sales': 0,
                'jp_sales': 0,
                'other_sales': 0,
            },
            'games_by_rating': [],
        })

    df = df.fillna({
        'publisher': 'Unknown',
        'rating': 'Unknown',
        'genre': 'Unknown'
    })

    df['critic_score'] = pd.to_numeric(df['critic_score'], errors='coerce').fillna(0)
    df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce').fillna(0)
    df['global_sales'] = pd.to_numeric(df['global_sales'], errors='coerce').fillna(0)

    total_games = len(df)
    total_global_sales = df['global_sales'].sum()

    avg_critic_score = df['critic_score'].mean()
    avg_user_score = df['user_score'].mean()

    top_games = (
        df.sort_values('global_sales', ascending=False)
        .head(10)
        .to_dict('records')
    )

    sales_by_genre = (
        df.groupby('genre')['global_sales']
        .sum()
        .reset_index()
        .rename(columns={'global_sales': 'total_sales'})
        .to_dict('records')
    )

    sales_by_platform = (
        df.groupby('platform')['global_sales']
        .sum()
        .reset_index()
        .rename(columns={'global_sales': 'total_sales'})
        .to_dict('records')
    )

    top_publishers = (
        df.groupby('publisher')['global_sales']
        .agg(total_sales='sum', game_count='count')
        .reset_index()
        .sort_values('total_sales', ascending=False)
        .head(10)
        .to_dict('records')
    )

    regional_sales = {
        'na_sales': df['na_sales'].sum(),
        'eu_sales': df['eu_sales'].sum(),
        'jp_sales': df['jp_sales'].sum(),
        'other_sales': df['other_sales'].sum(),
    }

    games_by_rating = (
        df.groupby('rating')
        .size()
        .reset_index(name='count')
        .to_dict('records')
    )

    return render(request, 'games/analytics.html', {
        'total_games': total_games,
        'total_global_sales': round(total_global_sales, 2),
        'avg_critic_score': round(avg_critic_score, 2),
        'avg_user_score': round(avg_user_score, 2),
        'top_games': top_games,
        'sales_by_genre': sales_by_genre,
        'sales_by_platform': sales_by_platform,
        'top_publishers': top_publishers,
        'regional_sales': regional_sales,
        'games_by_rating': games_by_rating,
    })