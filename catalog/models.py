from django.db import models  # Importing the models module from Django for defining database models
from django.db.models import UniqueConstraint  # Importing UniqueConstraint to define unique constraints on model fields
from django.db.models.functions import Lower  # Importing Lower to perform case-insensitive comparisons
from django.urls import reverse  # Importing reverse to generate URLs for model instances
import uuid  # Importing the uuid module for generating unique IDs


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,  # Ensures each genre name is unique
        help_text="Enter the book genre"
    )

    def __str__(self):
        return self.name  # Returns the name of the genre

    def get_absolute_url(self):
        return reverse("genre_detail", args=[str(self.id)])  # Returns the URL to view details of the genre
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),  # Case-insensitive uniqueness constraint on the 'name' field
                name='genre_name_case_insensitive_unique',
                violation_error_message="This Genre already exists.",
            ),
        ]


class Language(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,  # Ensures each language name is unique
        help_text="Enter a language name (e.g., English, French, Japanese)"
    )

    def __str__(self):
        return self.name  # Returns the name of the language

    def get_absolute_url(self):
        return reverse("language_detail", args=[str(self.id)])  # Returns the URL to view details of the language
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),  # Case-insensitive uniqueness constraint on the 'name' field
                name='language_name_case_insensitive_unique',
                violation_error_message="Language already exists.",
            ),
        ]


class Author(models.Model):
    fname = models.CharField('First Name', max_length=100)
    lname = models.CharField('Last Name', max_length=100)
    dob = models.DateField('Date of Birth', null=True, blank=True)
    dod = models.DateField('Date of Death', null=True, blank=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"  # Returns the full name of the author

    def get_absolute_url(self):
        return reverse("author_detail", args=[str(self.id)])  # Returns the URL to view details of the author
    
    class Meta:
        ordering = ['lname', 'fname']  # Specifies the default ordering of authors by last name and first name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, null=True)  # Defines a many-to-one relationship with Author model
    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the book",
        null=True
    )
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        unique=True,  # Ensures each ISBN is unique
        help_text="13 character ISBN"
    )
    genre = models.ManyToManyField(
        Genre,
        help_text="Select a genre for this book"
    )
    language = models.ForeignKey(Language, on_delete=models.RESTRICT, null=True)  # Defines a many-to-one relationship with Language model

    def __str__(self):
        return self.title  # Returns the title of the book

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])  # Returns the URL to view details of the book


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this transaction")  # Generates a UUID for each BookInstance
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)  # Defines a many-to-one relationship with Book model
    imprint = models.CharField(max_length=200, null=True, blank=True)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(
        max_length=1,
        blank=True,
        choices=LOAN_STATUS,
        default='m',
        help_text='Book availability',
    )

    def __str__(self):
        return f"{self.id} ({self.book.title})"  # Returns the ID and title of the book instance

    class Meta:
        ordering = ['due_back']  # Specifies the default ordering of book instances by due back date
