from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404

from accounts.models import User
from reviews.models import Ticket, Subscription

from reviews.forms import CreateTicketForm, SubscriptionForm


@login_required
def feed(request):
    followed_users = []
    for subscription in Subscription.objects.filter(user=request.user):
        followed_users.append(subscription.followed_user)
    tickets = []
    for ticket in Ticket.objects.all().order_by("-time_created"):
        if ticket.user in followed_users or ticket.user == request.user:
            tickets.append(ticket)
    context = {"tickets": tickets}
    return render(request, "reviews/feed.html", context)


@login_required
def create_ticket(request):
    form = CreateTicketForm()
    if request.method == "POST":
        form = CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            if "image" in request.FILES:
                ticket.image = request.FILES["image"]
            ticket.save()
            return redirect("feed")
    context = {"form": form}
    return render(request, "reviews/create_ticket_form.html", context)


@login_required
def subscriptions(request):
    form = SubscriptionForm()
    users = User.objects.all().order_by("username")
    context = {"form": form, "users": users}
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if username == request.user.username:
                error_message = "Vous ne pouvez pas vous abonner à vous même."
                context = {"form": form, "users": users, "error_message": error_message}
            else:
                try:
                    subscription = Subscription()
                    subscription.user = request.user
                    subscription.followed_user = User.objects.get(username=username)
                    subscription.save()
                except User.DoesNotExist:
                    error_message = "Cet utilisateur n'existe pas."
                    context = {"form": form, "users": users, "error_message": error_message}
                except IntegrityError:
                    error_message = "Vous êtes déjà abonné à cet utilisateur."
                    context = {"form": form, "users": users, "error_message": error_message}
    return render(request, "reviews/subscriptions.html", context)


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
