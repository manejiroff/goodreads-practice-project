from django.test import TestCase
from django.urls import reverse
from books.models import Book

class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:book-list'))

        self.assertContains(response, 'No books found.')
    
    def test_book_list(self):
        Book.objects.create(title='Book1', discription='description1', isbn='isbn1')
        Book.objects.create(title='Book2', discription='description2', isbn='isbn2')
        Book.objects.create(title='Book3', discription='description3', isbn='isbn3')

        response = self.client.get(reverse('books:book-list'))
        books = Book.objects.all()

        for book in books:
            self.assertContains(response, book.title)

    def test_book_detail_page(self):
        book = Book.objects.create(title='Book1', discription='description1', isbn='isbn1')

        response = self.client.get(reverse('books:book-detail', kwargs={'pk': book.id}))

        self.assertContains(response, book.title)

