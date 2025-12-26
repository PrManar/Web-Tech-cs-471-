
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name= "books.index"),
    path('list_books/', views.list_books, name= "books.list_books"),
    path('<int:bookId>/', views.viewbook, name="books.view_one_book"),
    path('aboutus/', views.aboutus, name="books.aboutus"),
    path('search/', views.search_books, name='search'),
    path('html5/links', views.links_page),
    path('html5/text/formatting', views.formatting_page),
    path('html5/listing', views.listing_page),
    path('html5/tables', views.tables_page),
    path('simple/query', views.simple_query, name='simple_query'),
    path('complex/query', views.complex_query, name='complex_query'),
    path('lab8/task1/', views.task1, name='task1'),
    path('lab8/task2/', views.task2, name='task2'),
    path('lab8/task3/', views.task3, name='task3'),
    path('lab8/task4/', views.task4, name='task4'),
    path('lab8/task5/', views.task5, name='task5'),
    path('lab8/task6/', views.task6, name='task6'),
    path('lab8/task7/', views.task7, name='task7'),
    path('lab9/task1', views.lab9task1, name='lab9_task1'),
    path('lab9/task2', views.lab9task2, name='lab9_task2'),
    path('lab9/task3', views.lab9task3, name='lab9_task3'),
    path('lab9/task4', views.lab9task4, name='lab9_task4'),
    path('lab9/task5', views.lab9task5, name='lab9_task5'),
    path('lab9/task6', views.lab9task6, name='lab9_task6'),
    # Part1 URLs (lab9_part1)
    path('lab9_part1/part1_listbooks/', views.listbooks_part1, name='listbooks_part1'),
    path('lab9_part1/addbook/', views.addbook_part1, name='addbook_part1'),
    path('lab9_part1/editbook/<int:id>/', views.editbook_part1, name='editbook_part1'),
    path('lab9_part1/deletebook/<int:id>/', views.deletebook_part1, name='deletebook_part1'),

    # Part2 URLs (lab9_part2) - using Django forms
    path('lab9_part2/listbooks/', views.listbooks_part2, name='listbooks_part2'),
    path('lab9_part2/addbook/', views.addbook_part2, name='addbook_part2'),
    path('lab9_part2/editbook/<int:id>/', views.editbook_part2, name='editbook_part2'),
    path('lab9_part2/deletebook/<int:id>/', views.deletebook_part2, name='deletebook_part2'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_add'),
    path('students/<int:pk>/edit/', views.student_update, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/many/', views.student2_list, name='student2_list'),
    path('students/many/add/', views.student2_create, name='student2_add'),
    path('students/many/<int:pk>/edit/', views.student2_update, name='student2_edit'),
    path('students/images/', views.item_image_list, name='item_image_list'),
    path('students/images/add/', views.item_image_create, name='item_image_add'),
]

