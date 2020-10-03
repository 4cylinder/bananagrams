from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

class CreateGameForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'createGameForm'
        self.helper.form_method = 'post'
        self.helper.form_action = "game:newgame"

        self.helper.add_input(Submit('submit', 'Create Game'))

    game_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'A Bananagrams Game'}))
    player_count = forms.ChoiceField(widget=forms.Select, choices=[(i, i) for i in range(2, 9)])
