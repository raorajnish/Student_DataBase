


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Classlist, Student, CIA, CIAP, Marks
from .forms import CreateClassForm, StudentForm, CIAForm, CIAPForm, MarksForm




def class_students(request, slug):
    class_instance = get_object_or_404(Classlist, slug=slug)
    students = Student.objects.filter(student_class=class_instance)
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.student_class = class_instance
            student.save()
            return redirect('myclass:class_students', slug=slug)
    else:
        form = StudentForm()

    return render(request, 'class_students.html', {
        'class_instance': class_instance,
        'students': students,
        'form': form
    })


# View to display a list of classes
def class_list(request):
    # Filter the classes to show only those added by the logged-in user
    user_classes = Classlist.objects.filter(author=request.user).order_by('-date')
    return render(request, 'class_list.html', {'classlists': user_classes})

# View to display a specific class page based on the slug
def class_page(request, slug):
    post = get_object_or_404(Classlist, slug=slug)
    students = Student.objects.filter(student_class=post)

    for student in students:
        # Use related_name from the Marks model to access related marks
        try:
            marks = student.marks
            student.cia_marks = marks.cia_marks
            student.ciap_marks = marks.ciap_marks
            student.mse_marks = marks.theory_marks - marks.cia_marks
            student.cgpa = marks.cgpa
        except Marks.DoesNotExist:
            student.cia_marks = 'NA'
            student.ciap_marks = 'NA'
            student.mse_marks = 'NA'
            student.cgpa = 'NA'

    return render(request, 'class_page.html', {'classlist': post, 'students': students})




# def class_page(request, slug):
#     post = get_object_or_404(Classlist, slug=slug) 
#     students = Student.objects.filter(student_class=post)# Use get_object_or_404 for better error handling
#     return render(request, 'class_page.html', {'classlist': post,'students': students,})

# View to create a new class (login required)
@login_required(login_url='users:login')
def class_new(request):
    if request.method == 'POST':
        form = CreateClassForm(request.POST, request.FILES)  # Handle POST data and files
        if form.is_valid():
            form.save()  # Save the form if it's valid
            return redirect('myclass:list')  # Redirect to the list of classes after saving
    else:
        form = CreateClassForm()  # If GET request, show an empty form

    return render(request, 'class_new.html', {'form': form})

def cia_marks_entry(request, slug, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = CIAForm(request.POST)
        if form.is_valid():
            cia = form.save(commit=False)
            cia.student = student
            cia.save()
            return redirect('success_url')
    else:
        form = CIAForm()

    return render(request, 'cia_marks_entry.html', {'form': form, 'student': student})

def ciap_marks_entry(request, slug, pk):
    student = get_object_or_404(Student, pk=pk)
    classlist = student.student_class
    if request.method == 'POST':
        form = CIAPForm(request.POST)
        if form.is_valid():
            ciap = form.save(commit=False)
            ciap.student = student
            ciap.save()
            return redirect('myclass:class_students', slug=slug)
    else:
        form = CIAPForm()

    return render(request, 'ciap_marks_entry.html', {'form': form, 'student': student, 'classlist': classlist})

def marks_entry(request, slug, pk):
    student = get_object_or_404(Student, pk=pk)
    classlist = student.student_class
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.save()
            return redirect('myclass:class_students', slug=slug)
    else:
        form = MarksForm()

    return render(request, 'marks_entry.html', {'form': form, 'student': student, 'classlist': classlist})



# def cia_marks_entry(request, slug, pk):
#     student = get_object_or_404(Student, pk=pk)  # Assuming you are linking to a student via slug
#     if request.method == 'POST':
#         form = CIAForm(request.POST)
#         if form.is_valid():
#             cia = form.save(commit=False)
#             cia.student = student  # Link the CIA record to the student
#             cia.save()
#             return redirect('success_url')  # Redirect to a success page or back to class page
#     else:
#         form = CIAForm()

#     return render(request, 'cia_marks_entry.html', {'form': form, 'student': student})

# def ciap_marks_entry(request, slug, pk):
#     student = get_object_or_404(Student, pk=pk)
#     classlist = student.student_class
    
#     if request.method == 'POST':
#         # Try to get the existing CIAP object, or create a new one if it doesn't exist
#         ciap, created = CIAP.objects.get_or_create(student=student)
        
#         # Update the fields with the data from the form
#         ciap.ciap_cce_attendance = request.POST.get('attendance')
#         ciap.writeup_and_experimentation = request.POST.get('writeup')
#         ciap.ciap_cce_component1 = request.POST.get('component1')
#         ciap.ciap_cce_component2 = request.POST.get('component2')

#         # Save the subcomponent marks
#         ciap.ciap_cce_component1_total_marks = request.POST.get('component1_total_marks')
#         ciap.ciap_cce_component2_total_marks = request.POST.get('component2_total_marks')
        
#         # Save the CIAP object to the database
#         ciap.save()

#         # Redirect back to the student's class page
#         return redirect('myclass:class_students', slug=slug)
    
#     return render(request, 'ciap_marks_entry.html', {'student': student, 'classlist': classlist})



# def marks_entry(request, slug, pk):
#     student = get_object_or_404(Student, pk=pk)
#     classlist = student.student_class
    
#     if request.method == 'POST':
#         # Process the form submission
#         marks = Marks.objects.get(student=student)
#         marks.ese = request.POST.get('ese')
#         marks.esep = request.POST.get('esep')
#         marks.save()
#         # Redirect back to the student's class page
#         return redirect('myclass:class_students', slug=slug)
    
#     return render(request, 'marks_entry.html', {'student': student, 'classlist': classlist})