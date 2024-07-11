from telnetlib import LOGOUT  # Importing LOGOUT from telnetlib module (unused in this code)
from django.shortcuts import render  # Importing the render function from Django shortcuts for rendering templates
from django.contrib.auth import login, authenticate  # Importing login and authenticate functions from Django authentication module
from . import forms  # Importing forms module from the current package
from django.http import HttpResponseRedirect  # Importing HttpResponseRedirect class from Django's HTTP module for redirection
from django.urls import reverse  # Importing reverse function from Django's URL module for generating URLs
from django.contrib.auth.mixins import LoginRequiredMixin  # Importing LoginRequiredMixin for requiring login
from django.contrib.auth import logout  # Importing logout function from Django authentication module


def logout_user(request):
    logout(request)  # Logging out the current user
    return HttpResponseRedirect(reverse('login'))  # Redirecting to the login page


def login_page(request):
    form = forms.LoginForm()  # Creating an instance of the LoginForm class
    login_msg = ""  # Initializing an empty login message
    if request.method == 'POST':  # Checking if the request method is POST
        form = forms.LoginForm(request.POST)  # Creating a LoginForm instance with the form data from the request
        if form.is_valid():  # Checking if the form data is valid
            user = authenticate(  # Authenticating the user with the provided credentials
                username=form.cleaned_data['username'],  # Retrieving the cleaned username from the form
                password=form.cleaned_data['password']  # Retrieving the cleaned password from the form
            )
            if user is not None:  # Checking if the user authentication was successful
                login(request, user)  # Logging in the authenticated user
                return HttpResponseRedirect(reverse('home_view'))  # Redirecting to the home page
            else:
                login_msg = "username/password invalid"  # Setting login message for invalid credentials
    return render(request, 'login.html', context={'form': form, 'login_msg': login_msg})  # Rendering the login page with form and login message context
