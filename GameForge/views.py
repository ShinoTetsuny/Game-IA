from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .story_generation import generate_game_concept_for_user
from .forms import GameConceptForm
from .models import GameConcept, StoryAct, Character, Location

# Create your views here.

def home_view(request):
    return render(request, 'GameForge/home.html')

@login_required
def dashboard_view(request):
    return render(request, 'GameForge/dashboard.html')

def generate_view(request):
    form = GameConceptForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        game = generate_game_concept_for_user(
            user=request.user,
            genre=data["genre"],
            ambiance=data["ambiance"],
            themes=data["themes"],
            references=data["references"]
        )

        return redirect("game_detail", game_id=game.id)  # Crée cette vue plus tard

    return render(request, "gameforge/generate.html", {"form": form})

def game_detail(request, game_id):
    game = get_object_or_404(GameConcept, pk=game_id, user=request.user)
    return render(request, "gameforge/detail.html", {"game": game})