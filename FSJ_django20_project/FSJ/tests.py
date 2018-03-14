from django.test import TestCase
from .models_student import Student
from .models_program import Program
from .models_yearofstudy import YearOfStudy
from django.contrib.auth.models import User
from django.test import Client
from django.db.models.deletion import ProtectedError

# Create your tests here.

class StudentModelTests(TestCase):
    
    def setUp(self):
        # Link FSJUser with a User model for authentication related business
        user = User.objects.create(username = "TestStudent", password = "studentpassword")    
        program = Program.objects.create(code = "SP", name = "StudentProgram")
        year = YearOfStudy.objects.create(year = "StudentYear")
        student = Student.objects.create(user = user, ccid = "TestStudent", first_name = "A", last_name = "Student", email = "astudent@test.com", ualberta_id = 1,
                               year = year, program = program)
        
        
    def test_student_retrieval(self):
        user = User.objects.get(username = "TestStudent")    
        program = Program.objects.get(code = "SP")
        year = YearOfStudy.objects.get(year = "StudentYear")
        student = Student.objects.get(ccid = "TestStudent")        
        
        self.assertEqual(student.ccid, "TestStudent")
        self.assertEqual(student.program, program)
        self.assertEqual(student.ccid, student.user.username)
        self.assertEqual(student.year, year)
        
        
    def test_program_delete(self):
        user = User.objects.get(username = "TestStudent")           
        year = YearOfStudy.objects.get(year = "StudentYear")
        Program.objects.get(code = "SP").delete()
        
        student = Student.objects.get(ccid = "TestStudent")  
        self.assertIsNone(student.program)
        
    
    def test_year_delete(self):
        
        with self.assertRaises(ProtectedError):
            YearOfStudy.objects.get(year = "StudentYear").delete()
            
        