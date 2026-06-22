from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Student, Book, Issue
from .forms import StudentForm, BookForm, IssueForm


# ── STUDENTS ──
def student_list(request):
    students = Student.objects.all()
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    return render(request, 'library/students.html', {'students': students, 'form': form})


def delete_student(request, pk):
    Student.objects.get(pk=pk).delete()
    return redirect('student_list')


# ── BOOKS ──
def book_list(request):
    books = Book.objects.all()
    total_available = sum(b.available for b in books)
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.available = book.quantity
            book.save()
            return redirect('book_list')
    return render(request, 'library/books.html', {
        'books': books,
        'form': form,
        'total_available': total_available,
    })


def delete_book(request, pk):
    Book.objects.get(pk=pk).delete()
    return redirect('book_list')


# ── ISSUE / RETURN ──
def issue_list(request):
    issues = Issue.objects.all().order_by('-issue_date')
    form = IssueForm()
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            if issue.book.available > 0:
                issue.book.available -= 1
                issue.book.save()
                issue.save()
            return redirect('issue_list')
    
    total_issued = issues.filter(status='issued').count()
    total_returned = issues.filter(status='returned').count()
    today = timezone.now().date()
    
    return render(request, 'library/issue.html', {
        'issues': issues,
        'form': form,
        'total_issued': total_issued,
        'total_returned': total_returned,
        'today': today,
    })


def return_book(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if issue.status == 'issued':
        issue.status = 'returned'
        issue.return_date = timezone.now().date()
        issue.book.available += 1
        issue.book.save()
        issue.save()
    return redirect('issue_list')