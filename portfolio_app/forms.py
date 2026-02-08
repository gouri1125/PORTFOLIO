# forms.py
from django import forms
from django.contrib.auth import get_user_model
# Delete CustomUserCreationForm - use Django's default
from django.contrib.auth.forms import UserCreationForm

# No custom form needed


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        # 🔐 force normal user
        user.is_superuser = False
        user.is_staff = False

        if commit:
            user.save()
        return user
