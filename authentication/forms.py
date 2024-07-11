from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput({'class':'form-control',
    'placeholder':'Enter Username'}),help_text='Enter Username')
    password = forms.CharField(max_length=25,widget=forms.PasswordInput
    ({'class':'form-control','placeholder':'Enter Password'}),help_text='Enter Password')