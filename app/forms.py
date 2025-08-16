from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (UserCreationForm, 
                                       AuthenticationForm,
                                       UsernameField,
                                       PasswordChangeForm,
                                       PasswordResetForm,
                                       SetPasswordForm)

from django.utils.translation import gettext,gettext_lazy as _

from .models import Customer
# ---------------------------------------- Register Form -------------------------------------------------
class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password',}),
        help_text=password_validation.password_validators_help_text_html(),
        )
    
    password2 = forms.CharField(
        label='Confirm Password', 
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}),
        help_text=_("Enter the same password as before, for verification."),
        )
    
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email','autofocus':True,}))
    class Meta:
        model = User
        fields = ['email','username',]
        labels = {'email':'Email'}
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Username','data-bs-toggle':'popover', 'title':'Username', 'data-bs-content':'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'}),

        }

# ---------------------------------------- Login Form -------------------------------------------------
class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget = forms.TextInput(attrs={'autocomplete':'off','class':'form-control','placeholder':'username'})
        )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control','placeholder':'Password'})
        )

# ---------------------------------- Password change Form ------------------------------------------------
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control','placeholder':'Old Password'})
        )
    new_password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control','placeholder':'New Password'}),
        help_text=password_validation.password_validators_help_text_html(),
        )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control','placeholder':'Confirm New Password'})
        )

# ---------------------------------- Password reset Form ------------------------------------------------
class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email",'class':'form-control','placeholder':'Email'}),
    )

# ------------------------------ Set reset password Form ------------------------------------------------

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class':'form-control','placeholder':'New password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class':'form-control','placeholder':'New password confirmation'}),
    )


# ---------------------------------- Edit user info Form ------------------------------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'First Name','required':True}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name','required':True}),
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Username','readonly':True}),
            'email': forms.TextInput(attrs={'class':'form-control','placeholder':'Email','readonly':True}),

        }

# ---------------------------------- Address Form ------------------------------------------------
class AddressForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ('name','city','district','zipcode')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'name',}),
            'city': forms.TextInput(attrs={'class':'form-control','placeholder':'city',}),
            'district': forms.Select(attrs={'class':'form-control','placeholder':'district',}),
            'zipcode': forms.NumberInput(attrs={'class':'form-control','placeholder':'zipcode',}),

        }
