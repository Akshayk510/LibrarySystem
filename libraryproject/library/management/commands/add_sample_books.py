from django.core.management.base import BaseCommand
from library.models import Book
import random

class Command(BaseCommand):
    help = 'Adds sample books to the library'

    def handle(self, *args, **kwargs):
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
            },
            {
                'title': 'The Hunger Games',
                'author': 'Suzanne Collins',
                'isbn': '9780439023481',
                'available': True
            },
            {
                'title': 'The Shining',
                'author': 'Stephen King',
                'isbn': '9780307743657',
                'available': True
            },
            {
                'title': 'Brave New World',
                'author': 'Aldous Huxley',
                'isbn': '9780060850524',
                'available': True
            },
            {
                'title': 'The Odyssey',
                'author': 'Homer',
                'isbn': '9780140268867',
                'available': True
            },
            {
                'title': 'Crime and Punishment',
                'author': 'Fyodor Dostoevsky',
                'isbn': '9780143107637',
                'available': True
            }
        ]

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
                self.stdout.write(self.style.SUCCESS(f'Added book: {book_data["title"]}'))
            else:
                books_skipped += 1
                self.stdout.write(self.style.WARNING(f'Skipped existing book: {book_data["title"]}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully added {books_added} books. Skipped {books_skipped} existing books.'))