# Generated by Django 5.2 on 2025-04-11 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameForge', '0003_alter_storyact_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameconcept',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='game_concepts/images/'),
        ),
    ]
