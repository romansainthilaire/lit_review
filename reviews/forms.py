from django import forms

from reviews.models import Ticket, Review


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


class CreateReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        labels = {
            "headline": "Titre",
            "rating": "Note",
            "body": "Commentaire"
            }
        widgets = {"body": forms.Textarea(attrs={"rows": "7"})}

    def __init__(self, *args, **kwargs):
        super(CreateReviewForm, self).__init__(*args, **kwargs)
        self.fields["headline"].widget.attrs["placeholder"] = ""
        self.fields["body"].widget.attrs["placeholder"] = ""


class SubscriptionForm(forms.Form):

    username = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}))
