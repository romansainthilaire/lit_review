from django.urls import path

from reviews import views

urlpatterns = [
    path("flux/", views.feed, name="feed"),
    path("ticket/nouveau/", views.create_ticket, name="create_ticket"),
    path("abonnements/", views.subscriptions, name="subscriptions"),
    path("desabonner/<int:followed_user_id>/", views.unsubscribe, name="unsubscribe"),
]
