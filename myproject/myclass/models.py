from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Validation functions
def validate_component2(value):
    if value > 20:
        raise ValidationError('Component 2 marks cannot exceed 20.')

def validate_component1(value):
    if value > 20:
        raise ValidationError('Component 1 marks cannot exceed 20.')

def validate_attendance(value):
    if value > 5:
        raise ValidationError('Attendance marks cannot exceed 5.')

def validate_writeup(value):
    if value > 5:
        raise ValidationError('Writeup and experimentation marks cannot exceed 5.')

def validate_cia_component1(value):
    if value > 20:
        raise ValidationError('Component 1 marks cannot exceed 20.')

def validate_cia_component2(value):
    if value > 20:
        raise ValidationError('Component 2 marks cannot exceed 20.')

def validate_cia_attendance(value):
    if value > 10:
        raise ValidationError('Attendance marks cannot exceed 10.')

def validate_ese(value):
    if value > 100:
        raise ValidationError('ESE marks cannot exceed 100.')
    
def validate_esep(value):
    if value > 100:
        raise ValidationError('ESEP marks cannot exceed 100.')
    
def validate_mse(value):
    if value > 20:
        raise ValidationError('MSE marks cannot exceed 20.')

# 1. Classlist
class Classlist(models.Model):
    title = models.CharField(max_length=75)
    branch = models.CharField(max_length=100, default=None, null=True, blank=True)
    subject = models.CharField(max_length=100, default=None, null=True, blank=True)
    academic_year = models.CharField(max_length=30, default=None, null=True, blank=True)
    slug = models.SlugField(unique=True, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# 2. Student
class Student(models.Model):
    name = models.CharField(max_length=100)
    prn = models.CharField(max_length=100, unique=True)  # Secondary candidate key
    srno = models.IntegerField(default=None, null=True, blank=True)
    register_number = models.IntegerField(primary_key=True)  # Primary key of Student class
    student_class = models.ForeignKey(Classlist, on_delete=models.CASCADE)
    slug2 = models.SlugField(blank=True)  # Joined slug of Classlist and Student


    def __str__(self):
        return self.name

class Marks(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='marks')
    pracs_marks = models.FloatField(default=0, null=True, blank=True)  # Sum of CIAP and ESEP
    theory_marks = models.FloatField(default=0, null=True, blank=True)  # Sum of CIA and ESE
    cia_marks = models.FloatField(default=0, null=True, blank=True)  # Sum of MSE and CIA_CCE_final
    ciap_marks = models.FloatField(default=0, null=True, blank=True)  # Equal to CIAP_CCE_final
    ese = models.FloatField(default=0,validators=[validate_ese])  # Marks directly entered for ESE (100m scale down to 60m)
    scaled_ese = models.FloatField(default=0,blank=True, null=True)  # Scaled value of ESE
    esep = models.FloatField(default=0,validators=[validate_esep])  # Marks directly entered for ESEP (100m scale down to 60m)
    scaled_esep = models.FloatField(default=0,blank=True, null=True)  # Scaled value of ESEP
    cgpa = models.FloatField(default=0, null=True, blank=True)  # CGPA calculated from theory and pracs marks

    def save(self, *args, **kwargs):
        # Automatically compute the scaled values
        self.scaled_ese = self.ese * 0.6
        self.scaled_esep = self.esep * 0.6
        
        # Compute theory marks as sum of CIA marks and scaled ESE
        self.theory_marks = self.cia_marks + self.scaled_ese
        
        # Compute pracs marks as sum of CIAP marks and scaled ESEP
        self.pracs_marks = self.ciap_marks + self.scaled_esep
        
        # Calculate CGPA (this is just a sample conversion, you should adjust it as needed)
        total_marks = self.theory_marks + self.pracs_marks
        self.cgpa = (total_marks / 100) * 10  # Assuming 100 marks scale for CGPA conversion

        super().save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        return f"Marks for {self.student.name}"
    
    
# 4. CIA (Continuous Internal Assessment)
class CIA(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mse = models.FloatField(validators=[validate_mse])  # Mid Sem Exam (20 marks)
    cia_cce_final = models.FloatField()  # Sum of CCE component1, component2, and attendance (50 marks scaled down to 20)
    cia_cce_component1 = models.FloatField(validators=[validate_cia_component1])
    cia_cce_component2 = models.FloatField(validators=[validate_cia_component2])
    cia_cce_attendance = models.FloatField(validators=[validate_cia_attendance])

    def save(self, *args, **kwargs):
        # Automatically compute CIA marks
        self.cia_cce_final = self.cia_cce_component1 + self.cia_cce_component2 + self.cia_cce_attendance
        super().save(*args, **kwargs)

        # Update the related Marks record
        try:
            marks_record = Marks.objects.get(student=self.student)
            marks_record.cia_marks = self.cia_cce_final + self.mse
            marks_record.save()
        except Marks.DoesNotExist:
            # Handle the case where Marks record does not exist
            pass

    def __str__(self):
        return f"CIA for {self.student.name}"

# 5. CIAP (Continuous Internal Assessment for Practicals)
class CIAP(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ciap_cce_final = models.FloatField()  # Sum of CCE component1, component2, attendance, writeup, and experimentation (50 marks scaled down to 40)
    ciap_cce_component1 = models.FloatField(validators=[validate_component1])
    ciap_cce_component2 = models.FloatField(validators=[validate_component2])
    ciap_cce_attendance = models.FloatField(validators=[validate_attendance])
    writeup_and_experimentation = models.FloatField(validators=[validate_writeup])

    def save(self, *args, **kwargs):
        # Compute the sum of components
        
        total = (self.ciap_cce_component1 + self.ciap_cce_component2 +
                 self.ciap_cce_attendance + self.writeup_and_experimentation)
        
        # Scale down the sum from 50 to 40
        self.ciap_cce_final = total * (40 / 50)
        
        # Save the model
        super().save(*args, **kwargs)
        
        # Update the related Marks record
        try:
            marks_record = Marks.objects.get(student=self.student)
            marks_record.ciap_marks = self.ciap_cce_final
            marks_record.pracs_marks = marks_record.ciap_marks + (marks_record.pracs_marks - getattr(marks_record, 'ciap_marks', 0))
            marks_record.save()
        except Marks.DoesNotExist:
            # Create a Marks record if it does not exist
            Marks.objects.create(student=self.student, ciap_marks=self.ciap_cce_final, pracs_marks=self.ciap_cce_final)

    def __str__(self):
        return f"CIAP for {self.student.name}"
