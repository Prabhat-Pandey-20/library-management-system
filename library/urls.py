from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('books/', views.book_list, name='book_list'),
    path('issue/', views.issue_list, name='issue_list'),
    path('delete-student/<int:pk>/', views.delete_student, name='delete_student'),
    path('delete-book/<int:pk>/', views.delete_book, name='delete_book'),
    path('return/<int:pk>/', views.return_book, name='return_book'),
]