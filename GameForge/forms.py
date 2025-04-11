from django import forms

class GameConceptForm(forms.Form):
    genre = forms.CharField(max_length=100, label='Genre', required=True)
    ambiance = forms.CharField(max_length=100, label='Ambiance', required=True)
    themes = forms.CharField(max_length=100, label='Theme', required=True, widget=forms.TextInput(attrs={"rws": 2}))
    references = forms.CharField(label='References', required=False, widget=forms.Textarea(attrs={"rows": 2}))