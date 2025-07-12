from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


# Optional: Remove this if you're only using `CustomRegisterForm`
# OR rename it and update its model
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # <-- fix here!
        fields = ['username', 'email', 'password1', 'password2']


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
