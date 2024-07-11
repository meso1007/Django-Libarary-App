from django.shortcuts import render, get_object_or_404  # Import render function to render templates and get_object_or_404 to get objects or return 404 error
from django.http import HttpResponse  # Import HttpResponse for sending HTTP responses
from django.template import loader  # Import loader for template loading
from .models import *  # Import all models from the current application
from django.views import generic  # Import generic views for class-based views

from django.shortcuts import get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Define a list of menu items to be used in the navigation menu
menu_items = [
    {'text': 'Home', 'urlName': '/'},  # Home menu item
    {'text': 'All Books', 'urlName': '/catalog/books/'},  # All Books menu item
    {'text': 'All Author', 'urlName': '#'},  # All Author menu item
    {'text': 'Log out', 'urlName': '/accounts/logout/'} 
    ]

class AuthorCreate(LoginRequiredMixin, generic.edit.CreateView):
    login_url = "/account/login"
    redirect_field_name = 'login'
    model = Author
    fields = ['fname', 'lname', 'dob', 'dod']
    initial = {'dob', '05/06/1986'}
    template_name = "author_form.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu-items"] = menu_items
        return context
    
    

@login_required(redirect_field_name='login')

    # return render(request, 'index.html', context=context)

# Define the home view function
def home_view(request):
    num_books = Book.objects.all().count()  # Count all books in the database
    num_instances = BookInstance.objects.all().count()  # Count all book instances in the database

    num_available_bookinstances = BookInstance.objects.filter(status__exact='a').count()  # Count all available book instances (status = 'a')
    num_authors = Author.objects.all().count()  # Count all authors in the database

    # Create context dictionary to pass data to the template
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_available_bookinstances': num_available_bookinstances,
        'num_authors': num_authors,
        'menu_items': menu_items,  # Pass menu items to the template
        'user': request.user
    }

    # Render the index.html template with the context data
    return render(request, 'index.html', context=context)

# Define the Book view class for listing all books
class Book_view(LoginRequiredMixin, generic.ListView):
    login_url = 'accounts/login/'
    redirect_field_name = 'login'
    model = Book  # Specify the model to be used
    context_object_name = 'book_list'  # Name of the context variable for the book list
    # queryset = Book.objects.filter(title__icontains='Positive')[:2]  # Example of filtering queryset (commented out)
    queryset = Book.objects.all()  # Queryset to get all books
    template_name = 'book_list.html'  # Specify the template to be used
    
    # Override get_context_data to add additional context data
    def get_context_data(self, **kwargs):
        context = super(Book_view, self).get_context_data(**kwargs)  # Call the base implementation
        context['menu_items'] = menu_items  # Add menu items to the context
        return context

# Commented out Book_Detail_View class
# class Book_Detail_View(generic.DetailView):
#     model = Book
#     template_name = 'book_detail.html'
#     def get_context_data(self, **kwargs):
#         context = super(Book_Detail_View,self).get_context_data(**kwargs)
#         context['menu_items'] = menu_items
#         return context

# Define the Author detail view class for showing author details
class Author_Detail(generic.DeleteView):
    model = Author  # Specify the model to be used
    template_name = 'author_detail.html'  # Specify the template to be used
    @login_required(redirect_field_name='login')    #to strict the access
    # Override get_context_data to add additional context data
    def get_context_data(self, **kwargs):
        context = super(Author_Detail, self).get_context_data(**kwargs)  # Call the base implementation
        context['menu_items'] = menu_items  # Add menu items to the context
        return context
    
@login_required(redirect_field_name='login')  #if we put it, we can't see any webpage befor login

# Define the Book detail view function
def Book_Detail_View(request, pk):
    book = get_object_or_404(Book, pk=pk)  # Get the book object by primary key or return 404 error
    context = {
        'book': book,  # Add book object to the context
        'menu_items': menu_items  # Add menu items to the context
    }
    # Render the book_detail.html template with the context data
    return render(request, 'book_detail.html', context=context)
