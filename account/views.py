from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import RegisterForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
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