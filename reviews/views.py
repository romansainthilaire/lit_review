from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404

from reviews.models import UserFollows

from reviews.forms import UserFollowsForm


@login_required
def user_follows(request):
    form = UserFollowsForm()
    context = {"form": form}
    if request.method == "POST":
        form = UserFollowsForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if username == request.user.username:
                error_message = "Vous ne pouvez pas vous abonner à vous même."
                context = {"form": form, "error_message": error_message}
            else:
                try:
                    user_follows = UserFollows()
                    user_follows.user = request.user
                    user_follows.followed_user = User.objects.get(username=username)
                    user_follows.save()
                except User.DoesNotExist:
                    error_message = "Cet utilisateur n'existe pas."
                    context = {"form": form, "error_message": error_message}
                except IntegrityError:
                    error_message = "Vous êtes déjà abonné à cet utilisateur."
                    context = {"form": form, "error_message": error_message}
    return render(request, "reviews/user_follows.html", context)


@login_required
def unsubscribe(request, followed_user_id):
    try:
        followed_user = User.objects.get(pk=followed_user_id)
    except User.DoesNotExist:
        raise Http404
    try:
        user_follows = UserFollows.objects.get(user=request.user, followed_user=followed_user)
    except UserFollows.DoesNotExist:
        raise Http404
    user_follows.delete()
    return redirect("user_follows")
