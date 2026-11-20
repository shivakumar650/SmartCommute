from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegistrationForm


class AccountLoginView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm

    def form_valid(self, form):
        messages.success(self.request, "Welcome back to SmartCommute.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


def register(request):
    if request.user.is_authenticated:
        return redirect("commute:dashboard")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account was created successfully.")
            return redirect("commute:dashboard")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})


@require_POST
def account_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")
