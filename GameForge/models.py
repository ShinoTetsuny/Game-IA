from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class GameConcept(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_concepts")
    description = models.TextField()
    genre = models.CharField(max_length=100)
    ambiance = models.CharField(max_length=100)
    themes = models.TextField(help_text="Thèmes ou mots-clés")
    references = models.TextField(blank=True, help_text="Références culturelles, jeux similaires")
    created_at = models.DateTimeField(auto_now_add=True)

    # Résumé de l'univers
    universe_description = models.TextField()

    def __str__(self):
        return self.title

class StoryAct(models.Model):
    game = models.ForeignKey(GameConcept, on_delete=models.CASCADE, related_name="story_acts")
    act_number = models.PositiveIntegerField()
    title = models.TextField()
    content = models.TextField()

    class Meta:
        ordering = ["act_number"]

    def __str__(self):
        return f"Acte {self.act_number} – {self.title}"

class Character(models.Model):
    game = models.ForeignKey(GameConcept, on_delete=models.CASCADE, related_name="characters")
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    background = models.TextField()
    abilities = models.TextField()

    def __str__(self):
        return self.name

class Location(models.Model):
    game = models.ForeignKey(GameConcept, on_delete=models.CASCADE, related_name="locations")
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name