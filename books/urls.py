from django.urls import path
from books import views

app_name = 'books'

urlpatterns = [
    path('', views.BookView.as_view(), name='book-list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book-detail')
]