# from django.urls import path
# from . import views

# app_name = 'myclass'

# urlpatterns = [
#     path('', views.class_list, name="list"),
#     path('new-class/', views.class_new, name="new-class"),
#     path('<slug:slug>/', views.class_page, name="page"),
#     path('<slug:slug>/students/', views.class_students, name="class_students"),
#     path('cia/', views.cia_marks_entry, name='cia_marks_entry'),
#     path('ciap/', views.ciap_marks_entry, name='ciap_marks_entry'),
#     path('marks/', views.marks_entry, name='marks_entry'),
# ]


from django.urls import path
from . import views

app_name = 'myclass'

urlpatterns = [
    path('', views.class_list, name="list"),
    path('new-class/', views.class_new, name="new-class"),
    path('<slug:slug>/', views.class_page, name="page"),  # Keep this as the last pattern
    path('<slug:slug>/students/', views.class_students, name="class_students"),
    path('<slug:slug>/students/<int:pk>/cia/', views.cia_marks_entry, name='cia_marks_entry'),  # Place these before the slug pattern
    path('<slug:slug>/students/<int:pk>/ciap/', views.ciap_marks_entry, name='ciap_marks_entry'),
    path('<slug:slug>/students/<int:pk>/marks/', views.marks_entry, name='marks_entry'),
]

