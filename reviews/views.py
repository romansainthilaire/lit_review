from itertools import chain

from django.db.models import CharField, Value, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404

from accounts.models import User
from reviews.models import Ticket, Review, Subscription

from reviews.forms import CreateTicketForm, CreateReviewForm, SubscriptionForm


@login_required
def feed(request):
    followed_users = [request.user]
    for subscription in Subscription.objects.filter(user=request.user):
        followed_users.append(subscription.followed_user)
    tickets = Ticket.objects.filter(user__in=followed_users)
    reviews = Review.objects.filter(Q(user__in=followed_users) | Q(ticket__user=request.user))
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
    context = {"posts": posts}
    return render(request, "reviews/feed.html", context)


@login_required
def posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(Q(user=request.user) | Q(ticket__user=request.user))
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
    context = {"posts": posts}
    return render(request, "reviews/posts.html", context)


@login_required
def create_ticket(request):
    ticket_form = CreateTicketForm()
    if request.method == "POST":
        ticket_form = CreateTicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            if "image" in request.FILES:
                ticket.image = request.FILES["image"]
            ticket.save()
            return redirect("feed")
    context = {"ticket_form": ticket_form}
    return render(request, "reviews/create_ticket_form.html", context)


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    review_form = CreateReviewForm()
    if request.method == "POST":
        review_form = CreateReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("feed")
    context = {"review_form": review_form, "ticket": ticket}
    return render(request, "reviews/create_review_form.html", context)


@login_required
def create_ticket_and_review(request):
    ticket_form = CreateTicketForm()
    review_form = CreateReviewForm()
    if request.method == "POST":
        ticket_form = CreateTicketForm(request.POST, request.FILES)
        review_form = CreateReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            if "image" in request.FILES:
                ticket.image = request.FILES["image"]
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("feed")
    context = {"ticket_form": ticket_form, "review_form": review_form}
    return render(request, "reviews/create_ticket_and_review_form.html", context)


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
    followed_user = get_object_or_404(User, pk=followed_user_id)
    try:
        subscription = Subscription.objects.get(user=request.user, followed_user=followed_user)
    except Subscription.DoesNotExist:
        raise Http404
    subscription.delete()
    return redirect("subscriptions")
