from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account successfully created for {username}!")
            return redirect("login")  # Change 'login' to your login URL name
    else:
        form = RegisterForm()
    return render(request, "account/register.html", {"form": form})

@login_required # This decorator ensures only logged-in users can access this page
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'templates/registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        messages.success(self.request, "Your password was successfully changed!")
        return super().form_valid(form)
