import re
import json
from PIL import Image
from io import BytesIO
from django.conf import settings
from huggingface_hub import InferenceClient
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
from .models import GameConcept, StoryAct, Character, Location

# Utiliser le token depuis settings.py
client = InferenceClient(
    provider="nebius",
    api_key=settings.HUGGINGFACE_TOKEN
)

def generate_game_concept_for_user(user, genre, ambiance, themes, references):
    prompt = (
        f"Generate a game {genre} with an ambiance {ambiance}, "
        f"in thoses themes : {themes}. "
    )
    if references:
        prompt += f"Use theses as references (if empty ingore this part) : {references}. "

    prompt += (
        "Give us a complete game concept with a detailed description of the universe, "
        "a list of 3 to 5 acts with a short description of each act, "
        "and a list of characters with their names, roles, abilities, and backgrounds. "
        "Also include a list of locations with their names and descriptions. "
        "The output should be in French. "
        "The output should be in JSON format, with the structure:"
        '{"title": "Title of the universe or story",'
        '"universe_description": "Brief description of the world or universe, its setting, atmosphere, and key conflicts.",'
        '"story_acts": ['
            '{'
            '"act_number": 1,'
            '"title": "Title of Act 1",'
            '"content": "Summary of the first act s plot, major events, and the protagonist s initial development."'
            '},'
            '{'
            '"act_number": 2,'
            '"title": "Title of Act 2",'
            '"content": "Summary of the second act s plot, challenges faced, character relationships, and revelations."'
            '},'
            '{'
            '"act_number": 3,'
            '"title": "Title of Act 3",'
            '"content": "Climax of the story, resolution of the main conflict, and the outcome based on the protagonist s choices."'
            '}'
        '],'
        '"characters": ['
            '{'
            '"name": "Character s name",'
            '"role": "Role in the story (Protagonist, Antagonist, etc.)",'
            '"abilities": "Powers, skills, or unique traits the character possesses",'
            '"background": "Origin story and background information of the character"'
            '}'
        '],'
        '"locations": ['
            '{'
            '"name": "Name of the location",'
            '"description": "Description of the environment, atmosphere, hazards, and its significance in the story"'
            '}'
        '],'
        '"image_prompt": "Detailed visual description of a key or representative scene from the universe, used for image generation (include art style, mood, setting, characters, and visual elements)"'
        '}'
        "You should send the JSON without any explanation or additional text. "
    )

    try:
        # Envoi à l'API
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.choices[0].message.content


        json_content = text.strip('```')
        json_content = json_content.strip('json')
        print(json_content)
        try:
            data = json.loads(json_content)
        except json.JSONDecodeError:
            print("Erreur JSON, contenu renvoyé:\n", text)
            return None

        # Créer l'objet principal
        game = GameConcept.objects.create(
            user=user,
            title=data.get("title", "Concept sans titre"),
            genre=genre,
            ambiance=ambiance,
            themes=themes,
            references=references,
            universe_description=data.get("universe_description", "")
        )

        for act in data.get("story_acts",[]):
            StoryAct.objects.create(
                game = game,
                act_number = act["act_number"],
                title = act["title"],
                content = act["content"],
            )
        
        for char in data.get("characters", []):
            Character.objects.create(
                game=game,
                name=char["name"],
                role=char["role"],
                abilities=char["abilities"],
                background=char["background"]
            )

        for loc in data.get("locations", []):
            Location.objects.create(
                game=game,
                name=loc["name"],
                description=loc["description"]
            )

        image_prompt = data.get("image_prompt", f"concept art of a {genre} game in {ambiance} style.")

        try:
            image_bytes = client.text_to_image(
                prompt=image_prompt,
                model="black-forest-labs/FLUX.1-dev",
            )
            print("Image generated successfully.")
            buffer = BytesIO()
            image_bytes.save(buffer, format="PNG")
            buffer.seek(0)
            # print("Image saved to buffer successfully.")
            game.image.save(game.title + ".webp", ContentFile(buffer.read()), save=True)
            print("Image saved to game model successfully.")
        except Exception as e:
            print("Erreur lors de la génération d'image :", e)

        return game
        
    except Exception as e:
        print(f"Error generating game concept: {e}")
        # En cas d'erreur, créer un concept de jeu minimal
        game = GameConcept.objects.create(
            user=user,
            title=f"{genre} – {ambiance}",
            genre=genre,
            ambiance=ambiance,
            themes=themes,
            references=references,
            universe_description="Une erreur est survenue lors de la génération du concept de jeu. Veuillez réessayer ultérieurement."
        )
        return game