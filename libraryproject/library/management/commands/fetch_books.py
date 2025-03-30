from django.core.management.base import BaseCommand
from library.models import Book
import requests
import json
import time

class Command(BaseCommand):
    help = 'Fetches books from Open Library API and adds them to the database'

    def add_arguments(self, parser):
        parser.add_argument('--subject', type=str, help='Subject to search for books')
        parser.add_argument('--limit', type=int, default=10, help='Number of books to fetch')

    def handle(self, *args, **kwargs):
        subject = kwargs.get('subject', 'fiction')
        limit = kwargs.get('limit', 10)
        
        self.stdout.write(self.style.SUCCESS(f'Fetching {limit} books on subject: {subject}'))
        
        # Open Library API URL
        url = f'https://openlibrary.org/subjects/{subject}.json?limit={limit}'
        
        try:
            response = requests.get(url)
            data = response.json()
            
            books_added = 0
            books_skipped = 0
            
            for work in data.get('works', []):
                title = work.get('title', 'Unknown Title')
                
                # Get authors
                authors = []
                for author in work.get('authors', []):
                    authors.append(author.get('name', 'Unknown Author'))
                
                author_str = ', '.join(authors) if authors else 'Unknown Author'
                
                # Generate a unique ISBN-like identifier based on the work key
                # (Open Library doesn't provide ISBNs in this API endpoint)
                work_key = work.get('key', '').replace('/works/', '')
                isbn = f'OL{work_key[:11]}' if work_key else f'OL{str(int(time.time()))}'
                
                # Check if book already exists
                if not Book.objects.filter(isbn=isbn).exists():
                    Book.objects.create(
                        title=title,
                        author=author_str,
                        isbn=isbn,
                        available=True
                    )
                    books_added += 1
                    self.stdout.write(self.style.SUCCESS(f'Added book: {title}'))
                else:
                    books_skipped += 1
                    self.stdout.write(self.style.WARNING(f'Skipped existing book: {title}'))
            
            self.stdout.write(self.style.SUCCESS(f'Successfully added {books_added} books. Skipped {books_skipped} existing books.'))
            
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error fetching books: {e}'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error parsing API response'))