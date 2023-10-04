from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.core.exceptions import ValidationError


class UserUpdateForm(forms.ModelForm):
 
    class Meta:
        model=User
        fields=['phone_number', 'national_id','email','username']
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists() and email!=self.instance.email:
            raise ValidationError('This email is already exist!')
        return email
    def clean_username(self):
        username=self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists() and username!=self.instance.username:
            raise ValidationError("This username is already exist!")
        return username
 


        


class UserRegisterForm(UserUpdateForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'national_id','password']
        widgets = {
            'password' : forms.PasswordInput ,
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if not password1 or not password2:
            raise forms.ValidationError('Enter the both of password')

        if password1 != password2:
            raise forms.ValidationError('Password must match')
        return cleaned_data
    
    
           
class UserLoginForm(forms.Form):
  
    username = forms.CharField(label='Username', max_length=80)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())