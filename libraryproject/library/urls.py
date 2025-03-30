from django.urls import path
from library import views

urlpatterns = [
    path('add-book/', views.add_book, name='add_book'),
    path('books/', views.book_list, name='book_list'),
    path('borrowed/', views.borrowed_books, name='borrowed_books'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('profile/', views.profile, name='profile'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('search/', views.search, name='search'),
]