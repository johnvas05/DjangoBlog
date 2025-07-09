from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import RegisterForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib import messages
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'register/register_done.html', {'new_user': form.cleaned_data['username']})
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})


@login_required #ensures only logged-in users can access this page
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


class CustomLogoutView(LogoutView):
    template_name = 'register/logged_out.html'

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'register/password_change_form.html'
    success_url   = reverse_lazy('account:password_change_done')

    def form_valid(self, form):
        messages.success(self.request, "Your password was successfully changed!")
        return super().form_valid(form)

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'register/password_change_done.html'




class CustomPasswordResetView(PasswordResetView):
    template_name            = 'register/password_reset_form.html'
    email_template_name      = 'register/password_reset_email.html'
    success_url              = reverse_lazy('account:password_reset_done')

    def get_subject(self):

        return "[My Blog] Reset your password"

    def form_valid(self, form):
        messages.success(self.request, "Password reset email sent!")
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'register/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'register/password_reset_confirm.html'
    success_url   = reverse_lazy('account:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'register/password_reset_complete.html'