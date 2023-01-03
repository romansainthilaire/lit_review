from django import forms


class SubscriptionForm(forms.Form):

    username = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}))
