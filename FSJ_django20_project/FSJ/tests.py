from django.test import TestCase
from .models_student import Student
from .models_program import Program
from .models_yearofstudy import YearOfStudy
from django.contrib.auth.models import User

# Create your tests here.

class StudentModelTests(TestCase):
    
    def setUp(self):
        # Link FSJUser with a User model for authentication related business
        self.user = User.objects.create(username = "Student")    
        self.program = Program.objects.create(code = "SP", name = "StudentProgram")
        self.year = YearOfStudy.objects.create(year = "StudentYear")
        self.student = Student.objects.create(user = self.user, ccid = "Student", first_name = "A", last_name = "Student", email = "astudent@test.com", ualberta_id = 1,
                               year = self.year, program = self.program)
        
        
    def test_student_retrieval(self):
        self.assertEqual(self.student.ccid, "Student")
        self.assertEqual(self.student.program, self.program)
        self.assertEqual(self.student.ccid, self.student.user.username)
        self.assertEqual(self.student.year, self.year)