from django import forms


class UserFollowsForm(forms.Form):

    username = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}))
