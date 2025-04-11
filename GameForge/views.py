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
    games = GameConcept.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'GameForge/dashboard.html', {'games': games})

def generate_view(request):
    if request.method == "POST":
        form = GameConceptForm(request.POST)
        if form.is_valid():
            game = generate_game_concept_for_user(
                request.user,
                form.cleaned_data["genre"],
                form.cleaned_data["ambiance"],
                form.cleaned_data["themes"],
                form.cleaned_data["references"]
            )
            if game:
                return redirect("game_detail", game_id=game.id)
            else:
                form.add_error(None, "La génération a échoué. L'IA n'a pas retourné de JSON valide.")
    else:
        form = GameConceptForm()
    return render(request, "gameforge/generate.html", {"form": form})

def game_detail(request, game_id):
    game = get_object_or_404(GameConcept, pk=game_id, user=request.user)
    return render(request, "gameforge/detail.html", {"game": game})