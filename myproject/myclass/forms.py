from django import forms
from .models import Classlist
from .models import Student
from .models import CIA, CIAP, Marks


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'prn', 'srno', 'register_number']  # Add any other fields you need
        widgets = {
            'prn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter PRN'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'srno': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sr. No'}),
            'register_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Register Number'}),
        }


class CreateClassForm(forms.ModelForm):
    class Meta:
        model = Classlist  # Use 'model' (singular) and refer to the Classlist class, not an instance
        fields = ['title', 'branch', 'subject','academic_year', 'slug', 'author']  # List the fields you want in the form
        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'aids-se5'}),
        }



# CIA Form
class CIAForm(forms.ModelForm):
    class Meta:
        model = CIA
        fields = ['mse', 'cia_cce_component1', 'cia_cce_component2', 'cia_cce_attendance']
        widgets = {
            'mse': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter MSE Marks'}),
            'cia_cce_component1': forms.NumberInput(attrs={ 'placeholder': 'Enter Component 1 Marks'}),
            'cia_cce_component2': forms.NumberInput(attrs={ 'placeholder': 'Enter Component 2 Marks'}),
            'cia_cce_attendance': forms.NumberInput(attrs={ 'placeholder': 'Enter Attendance Marks'}),
        }
# 

# CIAP Form
class CIAPForm(forms.ModelForm):
    class Meta:
        model = CIAP
        fields = ['ciap_cce_component1', 'ciap_cce_component2', 'ciap_cce_attendance', 'writeup_and_experimentation']
        widgets = {
            'ciap_cce_component1': forms.NumberInput(attrs={ 'placeholder': 'Enter Component 1 Marks'}),
            'ciap_cce_component2': forms.NumberInput(attrs={ 'placeholder': 'Enter Component 2 Marks'}),
            'ciap_cce_attendance': forms.NumberInput(attrs={ 'placeholder': 'Enter Attendance Marks'}),
            'writeup_and_experimentation': forms.NumberInput(attrs={ 'placeholder': 'Enter Writeup & Experimentation Marks'}),
        }

# ESE/ESEP Form
class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['ese', 'esep']
        widgets = {
            'ese': forms.NumberInput(attrs={ 'placeholder': 'Enter ESE Marks'}),
            'esep': forms.NumberInput(attrs={ 'placeholder': 'Enter ESEP Marks'}),
        }
