from django.shortcuts import render
from django.contrib.auth import authenticate, login

from accounts.forms import LoginForm


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
            else:
                error_message = "Identifiants invalides."
                context = {"form": form, "error_message": error_message}
    return render(request, "accounts/login_form.html", context)
