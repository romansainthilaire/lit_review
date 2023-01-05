from django.urls import path

from reviews import views

urlpatterns = [

    path("flux/", views.feed, name="feed"),
    path("posts/", views.posts, name="posts"),

    path("ticket/nouveau/", views.create_ticket, name="create_ticket"),
    path("ticket/<int:ticket_id>/modifier/", views.update_ticket, name="update_ticket"),

    path("critique/nouvelle/<int:ticket_id>/", views.create_review, name="create_review"),
    path("critique/<int:review_id>/modifier/", views.update_review, name="update_review"),

    path("critique/nouvelle/", views.create_ticket_and_review, name="create_ticket_and_review"),

    path("abonnements/", views.subscriptions, name="subscriptions"),
    path("desabonner/<int:followed_user_id>/", views.unsubscribe, name="unsubscribe"),

]
