from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Book, Borrow
from .forms import RegisterForm, BookForm
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, "library/home.html")

def book_list(request):
    books = Book.objects.all()  
    return render(request, 'library/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "library/book_detail.html", {"book": book})

@login_required
def borrow_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)

        # Check if the book is available
        if not book.available:
            messages.error(request, f'Sorry, "{book.title}" is currently not available.')
            return redirect('book_detail', book_id=book_id)

        # Update book availability and borrower
        book.available = False
        book.borrowed_by = request.user
        book.save()

        # Create a new borrow record
        borrow = Borrow.objects.create(
            user=request.user,
            book=book
        )

        messages.success(request, f'You have borrowed "{book.title}".')
        return redirect('book_list')

    return redirect('book_detail', book_id=book_id)

@login_required
def borrowed_books(request):
    borrowed_books = Borrow.objects.filter(user=request.user, returned_at=None)
    return render(request, "library/borrowed_books.html", {"borrowed_books": borrowed_books})

@login_required
def return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)
    if request.method == 'POST':
        # Update the borrow record
        borrow.returned_at = now()
        borrow.save()

        # Update book availability and clear borrower
        book = borrow.book
        book.available = True
        book.borrowed_by = None
        book.save()

        messages.success(request, f'You have successfully returned "{book.title}".')
        return redirect('borrowed_books')

    return render(request, "library/return_book.html", {"borrow": borrow})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = RegisterForm()
    return render(request, "library/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "library/login.html")

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully")
    return redirect('home')

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to the book list view
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})

@login_required
def profile(request):
    # Get currently borrowed books
    borrowed_books = Borrow.objects.filter(user=request.user, returned_at=None)

    # Get borrowing history (returned books)
    history = Borrow.objects.filter(user=request.user).exclude(returned_at=None).order_by('-returned_at')

    # Calculate statistics
    current_borrows = borrowed_books.count()
    total_borrows = Borrow.objects.filter(user=request.user).count()
    overdue_borrows = sum(1 for borrow in borrowed_books if borrow.is_overdue())

    context = {
        'borrowed_books': borrowed_books,
        'history': history,
        'current_borrows': current_borrows,
        'total_borrows': total_borrows,
        'overdue_borrows': overdue_borrows,
    }

    return render(request, 'library/profile.html', context)

@login_required
def recommendations(request):
    # Get user's borrowing history
    user_borrows = Borrow.objects.filter(user=request.user)

    # Get books the user has already borrowed
    borrowed_book_ids = user_borrows.values_list('book_id', flat=True)

    # Get recommendations based on user's reading history
    # This is a simple implementation - in a real system, you might use more sophisticated algorithms
    history_recommendations = []
    if borrowed_book_ids:
        # Get books with similar authors to what the user has borrowed
        borrowed_authors = Book.objects.filter(id__in=borrowed_book_ids).values_list('author', flat=True)
        history_recommendations = Book.objects.filter(author__in=borrowed_authors).exclude(id__in=borrowed_book_ids)[:6]

    # Get popular books (most borrowed)
    popular_books = Book.objects.exclude(id__in=borrowed_book_ids)[:6]

    # Get newest books
    new_arrivals = Book.objects.exclude(id__in=borrowed_book_ids).order_by('-id')[:6]

    context = {
        'history_recommendations': history_recommendations,
        'popular_books': popular_books,
        'new_arrivals': new_arrivals,
    }

    return render(request, 'library/recommendations.html', context)

def search(request):
    query = request.GET.get('q', '')
    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    isbn = request.GET.get('isbn', '')

    books = Book.objects.all()

    # Apply filters
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )

    if title:
        books = books.filter(title__icontains=title)

    if author:
        books = books.filter(author__icontains=author)

    if isbn:
        books = books.filter(isbn__icontains=isbn)

    # Pagination
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'books': page_obj,
        'query': query,
        'title': title,
        'author': author,
        'isbn': isbn,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }

    return render(request, 'library/search.html', context)
