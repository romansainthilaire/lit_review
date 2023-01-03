from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404

from reviews.models import Subscription

from reviews.forms import SubscriptionForm


@login_required
def feed(request):
    return render(request, "reviews/feed.html")


@login_required
def subscriptions(request):
    form = SubscriptionForm()
    context = {"form": form}
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if username == request.user.username:
                error_message = "Vous ne pouvez pas vous abonner à vous même."
                context = {"form": form, "error_message": error_message}
            else:
                try:
                    subscription = Subscription()
                    subscription.user = request.user
                    subscription.followed_user = User.objects.get(username=username)
                    subscription.save()
                except User.DoesNotExist:
                    error_message = "Cet utilisateur n'existe pas."
                    context = {"form": form, "error_message": error_message}
                except IntegrityError:
                    error_message = "Vous êtes déjà abonné à cet utilisateur."
                    context = {"form": form, "error_message": error_message}
    return render(request, "reviews/subscription.html", context)


@login_required
def unsubscribe(request, followed_user_id):
    try:
        followed_user = User.objects.get(pk=followed_user_id)
    except User.DoesNotExist:
        raise Http404
    try:
        subscription = Subscription.objects.get(user=request.user, followed_user=followed_user)
    except Subscription.DoesNotExist:
        raise Http404
    subscription.delete()
    return redirect("subscriptions")
