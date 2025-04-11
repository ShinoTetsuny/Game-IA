from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .story_generation import generate_game_concept_for_user
from .forms import GameConceptForm
from .models import GameConcept, StoryAct, Character, Location
from django.db.models import Count

# Create your views here.

def home_view(request):
    context = {}
    if request.user.is_authenticated:
        # Obtenir le nombre de jeux créés et restants pour l'utilisateur connecté
        games_count = GameConcept.objects.filter(user=request.user).count()
        max_games = 5
        remaining_games = max(0, max_games - games_count)
        context = {
            'games_count': games_count,
            'remaining_games': remaining_games
        }
    return render(request, 'GameForge/home.html', context)

@login_required
def dashboard_view(request):
    games = GameConcept.objects.filter(user=request.user).order_by('-created_at')
    games_count = games.count()
    max_games = 5
    remaining_games = max(0, max_games - games_count)
    
    return render(request, 'GameForge/dashboard.html', {
        'games': games,
        'games_count': games_count,
        'max_games': max_games,
        'remaining_games': remaining_games
    })

@login_required
def generate_view(request):
    # Vérifier combien de jeux l'utilisateur a déjà générés
    user_games_count = GameConcept.objects.filter(user=request.user).count()
    max_games = 5
    
    if user_games_count >= max_games:
        messages.error(request, f"Vous avez atteint la limite de {max_games} jeux générés. Vous ne pouvez pas en créer plus.")
        return redirect('dashboard')
    
    if request.method == "POST":
        form = GameConceptForm(request.POST)
        if form.is_valid():
            # Incrémenter le compteur d'API usage
            profile = request.user.profile
            profile.api_usage_count += 1
            profile.save()
            
            game = generate_game_concept_for_user(
                request.user,
                form.cleaned_data["genre"],
                form.cleaned_data["ambiance"],
                form.cleaned_data["themes"],
                form.cleaned_data["references"]
            )
            if game:
                messages.success(request, "Votre concept de jeu a été généré avec succès!")
                return redirect("game_detail", game_id=game.id)
            else:
                form.add_error(None, "La génération a échoué. L'IA n'a pas retourné de JSON valide.")
    else:
        form = GameConceptForm()
    
    # Informations sur les limites pour le template
    remaining_games = max(0, max_games - user_games_count)
    
    return render(request, "gameforge/generate.html", {
        "form": form,
        "remaining_games": remaining_games
    })

@login_required
def game_detail(request, game_id):
    game = get_object_or_404(GameConcept, pk=game_id, user=request.user)
    return render(request, "gameforge/detail.html", {"game": game})