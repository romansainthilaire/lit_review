from django.shortcuts import render


def log_in(request):
    return render(request, "accounts/login_form.html")
