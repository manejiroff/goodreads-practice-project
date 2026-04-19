from django.shortcuts import render
from django.views import View
from books.models import Book


class BookView(View):
    template_name = 'books/books.html'
    def get(self, request):
        return render(request, self.template_name, context={'books': Book.objects.all()})

class BookDetailView(View):
    template_name = 'books/books_detail.html'
    def get(self, request, pk):

        return render(request, self.template_name, context={'book': Book.objects.get(id=pk)})