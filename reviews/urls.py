from django.urls import path

from reviews import views

urlpatterns = [
    path("abonnements/", views.user_follows, name="user_follows"),
    path("desabonner/<int:followed_user_id>/", views.unsubscribe, name="unsubscribe"),
]
