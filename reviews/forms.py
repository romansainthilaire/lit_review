from django import forms

from reviews.models import Ticket


class CreateTicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        labels = {
            "title": "Titre",
            "description": "Description",
            "image": "Image de couverture"
            }
        widgets = {"description": forms.Textarea(attrs={"rows": "7"})}

    def __init__(self, *args, **kwargs):
        super(CreateTicketForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["placeholder"] = ""
        self.fields["description"].widget.attrs["placeholder"] = ""


class SubscriptionForm(forms.Form):

    username = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}))
