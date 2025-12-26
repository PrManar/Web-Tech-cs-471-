from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse

#from django.contrib.auth.decorators import login_required

#def index(request):
  #return HttpResponse("Hello, world")

def index(request):
  name = request.GET.get("name") or "world!"
  return render(request, "bookmodule/index.html", {"name": name})


def index2(request, val1 = 0):
    return HttpResponse("value1 = " + str(val1))

def viewbook(request, bookId):
  book1 = {'id':123, 'title': 'Continuous Delivery', 'author': 'J. Humble and D. Farley'}
  book2 = {'id':456, 'title': 'Secrets of Reverse Engineerings', 'author': 'E. Eliam'}
  targetbook = None
  if book1['id'] == bookId: targetbook = book1
  if book2['id'] == bookId: targetbook = book2
  context = {'book': targetbook}
  return render(request, 'bookmodule/show.html', context)


def index(request):
    return render(request, "bookmodule/index.html")
 
def list_books(request):
    return render(request, 'bookmodule/list_books.html')
 
def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')
 
def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')


from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def search_books(request):
    """
    - GET: render the form
    - POST: process form fields and render results (bookList.html)
    """
    if request.method == "POST":
        # Get keyword; default to empty string to avoid None
        keyword = (request.POST.get('keyword') or "").strip().lower()

        # Checkboxes: request.POST.get(...) returns 'on' when checked, or None when not
        is_title = request.POST.get('option1') is not None
        is_author = request.POST.get('option2') is not None

        # If neither checkbox selected, assume search both fields (optional)
        if not (is_title or is_author):
            is_title = is_author = True

        # Filter books
        books = __getBooksList()
        new_books = []
        for item in books:
            contained = False
            # compare lowercase for case-insensitive match
            if is_title and keyword and (keyword in item['title'].lower()):
                contained = True
            if not contained and is_author and keyword and (keyword in item['author'].lower()):
                contained = True

            # if keyword empty, you might want to show all or none; here we show all when keyword empty
            if not keyword:
                contained = True

            if contained:
                new_books.append(item)

        # Render result template with the found books
        return render(request, 'bookmodule/bookList.html', {'books': new_books, 'keyword': keyword})
    
    return render(request, 'bookmodule/search.html')
    
def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

    # GET -> show form
    return render(request, 'bookmodule/search.html')

def links_page(request):
    return render(request, 'bookmodule/books/html5/links.html')

def formatting_page(request):
    return render(request, 'bookmodule/books/html5/formatting.html')

def listing_page(request):
    return render(request, 'bookmodule/books/html5/listing.html')

def tables_page(request):
    return render(request, 'bookmodule/books/html5/tables.html')


from .models import Book

def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')  # case-insensitive search
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def complex_query(request):
    mybooks = Book.objects.filter(author__isnull=False) \
                          .filter(title__icontains='and') \
                          .filter(edition__gte=2) \
                          .exclude(price__lte=100)[:10]
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')


from django.db.models import Q

#lab 8:

def task1(request):
    # Query: price less than or equal to 80
    qs = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/books/lab8/list_books.html', {'objects': qs, 'title': 'Task 1: Price <= 80'})

def task2(request):
    q_co_in_title = Q(title__icontains='co')
    q_co_in_author = Q(author__icontains='co')
    qs = Book.objects.filter(Q(edition__gt=3) & (q_co_in_title | q_co_in_author))
    return render(request, 'bookmodule/books/lab8/list_books.html', {'objects': qs, 'title': 'Task 2: edition>3 and contains "co"'})

def task3(request):
    q_co_title = Q(title__icontains='co')
    q_co_author = Q(author__icontains='co')
    # opposite: edition <= 3 AND NOT(title contains 'co') AND NOT(author contains 'co')
    qs = Book.objects.filter(Q(edition__lte=3) & ~q_co_title & ~q_co_author)
    return render(request, 'bookmodule/books/lab8/list_books.html', {'objects': qs, 'title': 'Task 3: Not edition>3 and not contains "co"'})

def task4(request):
    qs = Book.objects.all().order_by('title')  # ascending
    # for descending: order_by('-title')
    return render(request, 'bookmodule/books/lab8/list_books.html', {'objects': qs, 'title': 'Task 4: Ordered by title'})

from django.db.models import Count, Sum, Avg, Max, Min

def task5(request):
    agg = Book.objects.aggregate(
        count=Count('id'),
        total=Sum('price'),
        avg=Avg('price'),
        max=Max('price'),
        min=Min('price')
    )
    # aggregate returns None for empty sets — handle gracefully in template
    return render(request, 'bookmodule/books/lab8/stats.html', {'stats': agg})


# apps/bookmodule/views.py

from django.core.exceptions import ImproperlyConfigured

# import your models (adjust import path if your models live elsewhere)
try:
    from .models import Address, Student
except Exception as e:
    Address = None
    Student = None
    _models_import_error = e

# existing views (task1, task2, ...) remain above/below this

def task6(request):
    """
    Shows the Student and Address models (Task 6).
    If the models are not present or migrations haven't been run, shows helpful message.
    """
    if Address is None or Student is None:
        # Helpful error page rather than raising AttributeError
        msg = (
            "Student/Address models could not be imported. "
            "Check apps/bookmodule/models.py and run migrations. "
            f"Import error: {_models_import_error}"
        )
        return HttpResponse(msg, status=500)

    # Query data to show (safe — will return empty querysets if none)
    addresses = Address.objects.all()
    students = Student.objects.select_related('address').all()

    return render(request, 'bookmodule/books/lab8/task6.html', {
        'addresses': addresses,
        'students': students,
        'title': 'Task 6 — Students and Addresses'
    })



from django.db.models import Count

def task7(request):
    # Group by address__city and annotate counts
    city_counts = (Student.objects
                   .values('address__city')
                   .annotate(num_students=Count('id'))
                   .order_by('-num_students'))  # optional ordering
    # city_counts is a QuerySet of dicts: {'address__city': 'Riyadh', 'num_students': 2}
    return render(request, 'bookmodule/books/lab8/city_counts.html', {'city_counts': city_counts, 'title': 'Students per City'})


from django.db.models import (
    Sum, F, Value, FloatField, ExpressionWrapper,
    Avg, Min, Max, Count, Q, Subquery, OuterRef
)
from .models import Book, Publisher

def lab9task1(request):
    total = Book.objects.aggregate(total=Sum('quantity'))['total'] or 0
    if total == 0:
        # avoid division by zero: set availability to 0
        books = Book.objects.all().annotate(availability=Value(0.0, output_field=FloatField()))
    else:
        books = Book.objects.all().annotate(
            availability=ExpressionWrapper(
                F('quantity') * Value(100.0) / Value(float(total)),
                output_field=FloatField()
            )
        )
    return render(request, 'bookmodule/books/lab9/task1.html', {'books': books, 'total': total})

def lab9task2(request):
    publishers = Publisher.objects.annotate(total_stock=Sum('book__quantity'))
    return render(request, 'bookmodule/books/lab9/task2.html', {'publishers': publishers})

def lab9task3(request):
    oldest_book_title = Book.objects.filter(publisher=OuterRef('pk')).order_by('pubdate').values('title')[:1]
    oldest_book_date = Book.objects.filter(publisher=OuterRef('pk')).order_by('pubdate').values('pubdate')[:1]

    publishers = Publisher.objects.annotate(
        oldest_title=Subquery(oldest_book_title),
        oldest_pubdate=Subquery(oldest_book_date)
    )
    return render(request, 'bookmodule/books/lab9/task3.html', {'publishers': publishers})

def lab9task4(request):
    publishers = Publisher.objects.annotate(
        avg_price=Avg('book__price'),
        min_price=Min('book__price'),
        max_price=Max('book__price')
    )
    return render(request, 'bookmodule/books/lab9/task4.html', {'publishers': publishers})

def lab9task5(request):
    high_rating_q = Q(book__rating__gte=4)   
    publishers = Publisher.objects.annotate(
        highly_rated_count=Count('book', filter=high_rating_q)
    )
    return render(request, 'bookmodule/books/lab9/task5.html', {'publishers': publishers})

def lab9task6(request):
    cond = Q(book__price__gt=50) & Q(book__quantity__gte=1) & Q(book__quantity__lt=5)
    publishers = Publisher.objects.annotate(
        filtered_count=Count('book', filter=cond)
    )
    return render(request, 'bookmodule/books/lab9/task6.html', {'publishers': publishers})

def listbooks_part1(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/books/lab9_part1/part1_listbooks.html', {'books': books})

# Part1 - add
def addbook_part1(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        publication_date = request.POST.get('publication_date') or None
        price = request.POST.get('price') or None
        isbn = request.POST.get('isbn')

        book = Book(
            title=title,
            author=author,
            publisher=publisher,
            publication_date=publication_date if publication_date else None,
            price=price if price else None,
            isbn=isbn
        )
        book.save()
        return redirect('bookmodule:books:lab9_part1:listbooks_part1')
    return render(request, 'bookmodule/books/lab9_part1/part1_addbook.html')

# Part1 - edit
def editbook_part1(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publisher = request.POST.get('publisher')
        pub_date = request.POST.get('publication_date') or None
        book.publication_date = pub_date
        book.price = request.POST.get('price') or None
        book.isbn = request.POST.get('isbn')
        book.save()
        return redirect('bookmodule:books:lab9_part1:listbooks_part1')
    return render(request, 'bookmodule/books/part1_editbook.html', {'book': book})

# Part1 - delete
def deletebook_part1(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == 'POST':
        book.delete()
        return redirect('bookmodule:books:lab9_part1:listbooks_part1')
    return render(request, 'bookmodule/books/confirm_delete.html', {'object': book, 'back_url': 'books:listbooks_part1'})




from .forms import BookForm

def listbooks_part2(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/books/lab9_part2/part2_listbooks.html', {'books': books})

def addbook_part2(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books:listbooks_part2')
    else:
        form = BookForm()
    return render(request, 'bookmodule/books/lab9_part2/part2_book_form.html', {'form': form, 'action': 'Add'})

def editbook_part2(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:listbooks_part2')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookmodule/books/lab9_part2/part2_book_form.html', {'form': form, 'action': 'Edit'})

def deletebook_part2(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == 'POST':
        book.delete()
        return redirect('books:listbooks_part2')
    return render(request, 'bookmodule/books/lab9_part2/confirm_delete.html', {'object': book, 'back_url': 'books:listbooks_part2'})


from .models import Student, Address
from .forms import StudentForm, AddressForm


def student_list(request):
    students = Student.objects.all()
    return render(request, 'bookmodule/students/student_list.html', {'students': students})


def student_create(request):
    if request.method == 'POST':
        sform = StudentForm(request.POST)
        aform = AddressForm(request.POST)
        if sform.is_valid() and aform.is_valid():
            addr = aform.save()
            student = sform.save(commit=False)
            student.address = addr
            student.save()
            return redirect('student_list')
    else:
        sform = StudentForm()
        aform = AddressForm()
    return render(request, 'bookmodule/students/student_form.html', {'sform': sform, 'aform': aform})


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    addr = student.address or Address()
    if request.method == 'POST':
        sform = StudentForm(request.POST, instance=student)
        aform = AddressForm(request.POST, instance=addr)
        if sform.is_valid() and aform.is_valid():
            addr = aform.save()
            student = sform.save(commit=False)
            student.address = addr
            student.save()
            return redirect('student_list')
    else:
        sform = StudentForm(instance=student)
        aform = AddressForm(instance=addr)
    return render(request, 'bookmodule/students/student_form.html', {'sform': sform, 'aform': aform, 'student': student})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'bookmodule/students/student_confirm_delete.html', {'student': student})

from .models import Student2, Address2
from .forms import Student2Form

def student2_list(request):
    students = Student2.objects.prefetch_related('addresses').all()
    return render(request, 'bookmodule/students/student2_list.html', {'students': students})

def student2_create(request):
    if request.method == 'POST':
        form = Student2Form(request.POST)
        if form.is_valid():
            student = form.save()
            form.save_m2m()
            return redirect('students:student2_list')
    else:
        form = Student2Form()
    return render(request, 'bookmodule/students/student2_form.html', {'form': form})

def student2_update(request, pk):
    student = get_object_or_404(Student2, pk=pk)
    if request.method == 'POST':
        form = Student2Form(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            form.save_m2m()
            return redirect('students:student2_list')
    else:
        form = Student2Form(instance=student)
    return render(request, 'bookmodule/students/student2_form.html', {'form': form, 'student': student}) 

from .models import ItemImage
from .forms import ItemImageForm

def item_image_list(request):
    images = ItemImage.objects.all()
    return render(request, 'bookmodule/students/item_image_list.html', {'images': images})

def item_image_create(request):
    if request.method == 'POST':
        form = ItemImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('students:item_image_list')
    else:
        form = ItemImageForm()
    return render(request, 'bookmodule/students/item_image_form.html', {'form': form})



