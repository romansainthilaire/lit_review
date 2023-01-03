from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from accounts.forms import LoginForm, RegistrationForm


def log_in(request):
    form = LoginForm()
    context = {"form": form}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("feed")
            else:
                error_message = "Identifiants invalides."
                context = {"form": form, "error_message": error_message}
    return render(request, "accounts/login_form.html", context)


@login_required
def log_out(request):
    logout(request)
    return redirect("login")


def registration(request):
    form = RegistrationForm()
    context = {"form": form}
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
        else:
            context["form"] = form
    return render(request, "accounts/registration_form.html", context)
