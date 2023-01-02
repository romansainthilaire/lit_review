from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={"placeholder": ""}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={"placeholder": ""}))
