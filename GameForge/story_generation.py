import re
from django.conf import settings
from huggingface_hub import InferenceClient
from .models import GameConcept, StoryAct, Character, Location

client = InferenceClient(
    provider="novita",
    api_key=""
    )

def generate_game_concept_for_user(user, genre, ambiance, themes, references):
    print(client)
    print(f"Generating game concept for user {user.username}...")
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
        "The output should be in a structured format, "
        "with sections clearly labeled for each part of the game concept. "
        "The output should be in French. "
        "It should feels like a game concept document. "
    )

    # Envoi à l'API
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3-0324",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content

    # --- Parsing rudimentaire (exemple à adapter selon le format réel) ---
    def extract_section(title, content):
        pattern = rf"{title}.*?\n(.*?)\n(?:\w|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    # Créer l'objet principal
    game = GameConcept.objects.create(
        user=user,
        description=f"{genre} – {ambiance}",
        genre=genre,
        ambiance=ambiance,
        themes=themes,
        references=references,
        universe_description=extract_section("Univers", text)
    )

    # Extraire les actes
    act_matches = re.findall(r"(Acte\s\d+.*?)\n(.+?)\n(.*?)\n", text, re.DOTALL | re.IGNORECASE)
    for i, (act_title, act_name, act_content) in enumerate(act_matches, start=1):
        StoryAct.objects.create(
            game=game,
            act_number=i,
            title=act_name.strip(),
            content=act_content.strip()
        )

        # Personnages (à adapter si IA retourne une liste)
    char_matches = re.findall(r"Nom : (.*?)\nRôle : (.*?)\nCapacités : (.*?)\nHistoire : (.*?)\n", text, re.DOTALL)
    for name, role, abilities, background in char_matches:
        Character.objects.create(
            game=game,
            name=name.strip(),
            role=role.strip(),
            abilities=abilities.strip(),
            background=background.strip()
        )

    # Lieux
    loc_matches = re.findall(r"Nom : (.*?)\nDescription : (.*?)\n", text, re.DOTALL)
    for name, desc in loc_matches:
        Location.objects.create(
            game=game,
            name=name.strip(),
            description=desc.strip()
        )

    return game