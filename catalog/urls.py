from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view, name='home_view'),
    path('books/', views.Book_view.as_view(),name='books'),
    path('books/<int:pk>',views.Book_Detail_View,name='book_detail'),
    path('author/<int:pk>',views.Author_Detail.as_view(), name='author_detail'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create')
]
