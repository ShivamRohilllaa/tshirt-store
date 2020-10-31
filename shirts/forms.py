from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomerCreationForm(UserCreationForm):
    username = forms.EmailField(max_length=50, label="Email",
        # widget= forms.EmailInput(attrs={'class':'form-control'})
        ) #Isme emailfield isliye liye hai qki humne isme username use ni kiya isme, username ki jagah humne isme email use ki hai to that's why we use this!!
    
    first_name = forms.CharField(max_length=50,
        # widget= forms.TextInput(attrs={'class':'form-control'})
        )
    
    last_name = forms.CharField(max_length=50,
        # widget= forms.TextInput(attrs={'class':'form-control'})
    )
    
    password1 = forms.PasswordInput(
        # widget= forms.PasswordInput(attrs={'class':'form-control'})
                           )
    
    password2 = forms.PasswordInput(
        # widget= forms.PasswordInput(attrs={'class':'form-control'})
        )

    #Apply Validations on a particular field

    def clean_first_name(self):
        value = self.cleaned_data.get('first_name')
        if len(value.strip()) < 4:
            raise ValidationError("Please Enter 4 Character Name") 

    def clean_last_name(self):
        value = self.cleaned_data.get('last_name')
        if len(value.strip()) < 4:
            raise ValidationError("Please Enter 4 Character Name") 
        

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name','last_name', 'password1', 'password2')


class Customerloginform(AuthenticationForm):
    username = forms.EmailField(required=True, label="Email") #Isme emailfield isliye liye hai qki humne isme username use ni kiya isme, username ki jagah humne isme email use ki hai to that's why we use this!!
    password = forms.PasswordInput()