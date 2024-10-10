from django.contrib import admin
from .models import Student, Classlist

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'prn', 'register_number', 'student_class','slug2')
    search_fields = ('name', 'prn', 'register_number')
    list_filter = ('student_class',)
    ordering = ('name',)

@admin.register(Classlist)
class ClasslistAdmin(admin.ModelAdmin):
    list_display = ('title', 'branch', 'subject', 'academic_year', 'author')
    search_fields = ('title', 'branch', 'subject', 'author__username')
    list_filter = ('branch', 'academic_year')
    ordering = ('title',)
