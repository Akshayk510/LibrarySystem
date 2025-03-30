from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta

def get_due_date():
    return now() + timedelta(days=14)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    available = models.BooleanField(default=True)
    borrowed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='borrowed_books')

    def __str__(self):
        return self.title

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=get_due_date)
    returned_at = models.DateTimeField(null=True, blank=True)

    def is_overdue(self):
        return self.returned_at is None and now() > self.due_date
