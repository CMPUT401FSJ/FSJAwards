from django.test import TestCase
from .models import Student
from .models import Program
from .models import YearOfStudy

# Create your tests here.

class StudentModelTests(TestCase):
    
    def setUp(self):
        Program.objects.create(code = "SP", name = "StudentProgram")
        YearOfStudy.objects.create(year = "StudentYear")
        Student.objects.create(ccid = "Student", first_name = "A", last_name = "Student", email = "astudent@test.com", ualberta_id = 1,
                               year = "F1", program = "P1")