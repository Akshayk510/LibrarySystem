"""
This script adds sample books to the library database.
Run this script with:
    python add_books_script.py
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libraryproject.settings')
django.setup()

# Import the Book model
from library.models import Book

# List of sample books with their details
sample_books = [
    {
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'isbn': '9780061120084',
        'available': True
    },
    {
        'title': '1984',
        'author': 'George Orwell',
        'isbn': '9780451524935',
        'available': True
    },
    {
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'isbn': '9780743273565',
        'available': True
    },
    {
        'title': 'Pride and Prejudice',
        'author': 'Jane Austen',
        'isbn': '9780141439518',
        'available': True
    },
    {
        'title': 'The Catcher in the Rye',
        'author': 'J.D. Salinger',
        'isbn': '9780316769488',
        'available': True
    },
    {
        'title': 'The Hobbit',
        'author': 'J.R.R. Tolkien',
        'isbn': '9780547928227',
        'available': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J.K. Rowling',
        'isbn': '9780747532743',
        'available': True
    },
    {
        'title': 'The Lord of the Rings',
        'author': 'J.R.R. Tolkien',
        'isbn': '9780618640157',
        'available': True
    },
    {
        'title': 'The Alchemist',
        'author': 'Paulo Coelho',
        'isbn': '9780062315007',
        'available': True
    },
    {
        'title': 'The Da Vinci Code',
        'author': 'Dan Brown',
        'isbn': '9780307474278',
        'available': True
    }
]

def add_books():
    books_added = 0
    books_skipped = 0

    for book_data in sample_books:
        # Check if book with this ISBN already exists
        if not Book.objects.filter(isbn=book_data['isbn']).exists():
            Book.objects.create(
                title=book_data['title'],
                author=book_data['author'],
                isbn=book_data['isbn'],
                available=book_data['available']
            )
            books_added += 1
            print(f'Added book: {book_data["title"]}')
        else:
            books_skipped += 1
            print(f'Skipped existing book: {book_data["title"]}')

    print(f'Successfully added {books_added} books. Skipped {books_skipped} existing books.')

if __name__ == '__main__':
    add_books()