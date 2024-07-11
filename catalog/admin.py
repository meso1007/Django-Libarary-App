from django.contrib import admin
from .models import *

# Define a custom ModelAdmin class for displaying Book model in admin
class BookDisplay(admin.ModelAdmin):
    list_display=('title','author')  # Specify which fields to display in the book list view in admin

# Define a custom ModelAdmin class for displaying BookInstance model in admin
class BookInstanceDisplay(admin.ModelAdmin):
    list_display =("book","status","due_back", "id")  # Specify which fields to display in the book instance list view in admin
    list_filter=("status","due_back")  # Add filters for status and due_back fields in the book instance list view

# Register the Book model with the custom BookDisplay admin class
admin.site.register(Book,BookDisplay)

# Register the Author, Genre, and Language models without any custom admin configuration
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)

# Register the BookInstance model with the custom BookInstanceDisplay admin class
admin.site.register(BookInstance,BookInstanceDisplay)
