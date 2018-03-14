from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from .models import Adjudicator, Coordinator, Student, Program, YearOfStudy
from django.test import Client
from django.db.models.deletion import ProtectedError


class AdjudicatorModelTests(TestCase):
    
    def setUp(self):
        self.ccid = "Adjudicator"
        self.first_name = "An"
        self.last_name = "Adjudicator"
        self.email = "anAdjudicator@test.com"
        self.ualberta_id = 1 
        Adjudicator.objects.create(ccid = self.ccid, first_name = self.first_name, 
                                   last_name = self.last_name, email = self.email, ualberta_id = self.ualberta_id)
        
    def test_get_adjudicator(self):
        obj = Adjudicator.objects.get(ccid = self.ccid)
        
        self.assertEqual(obj.ccid, self.ccid)
        self.assertEqual(obj.first_name, self.first_name)
        self.assertEqual(obj.last_name, self.last_name)
        self.assertEqual(obj.email, self.email)
        self.assertEqual(obj.ualberta_id, self.ualberta_id)
    
    def test_create_duplicate_adjudicator(self):  
        with self.assertRaises(IntegrityError):
            Adjudicator.objects.create(ccid = self.ccid)
        with self.assertRaises(IntegrityError):
            Adjudicator.objects.create(ualberta_id = self.ualberta_id)        
            
    def test_user_model_is_created_with_adjudicator(self):
        obj = Adjudicator.objects.get(ccid = self.ccid)
        user = obj.user
        self.assertEqual(user.username, obj.ccid)
        
    def test_user_model_is_correct_for_adjudicator(self):
        obj = Adjudicator.objects.get(ccid = self.ccid)
        user = obj.user
        user2 = User.objects.get(username = self.ccid)
        self.assertEqual(user, user2)
        
    def test_delete_adjudicator(self):
        obj = Adjudicator.objects.get(ccid = self.ccid)
        ccid = obj.ccid
        self.assertIsNotNone(obj)
        user = User.objects.get(username = self.ccid)
        self.assertIsNotNone(user)
        obj.delete()
        with self.assertRaises(Adjudicator.DoesNotExist):
            obj = Adjudicator.objects.get(ccid = self.ccid)
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username = self.ccid)
            

class CoordinatorModelTests(TestCase):
    
    def setUp(self):
        self.ccid = "Coordinator"
        self.first_name = "A"
        self.last_name = "Coordinator"
        self.email = "aCoordinator@test.com"
        self.ualberta_id = 1 
        Coordinator.objects.create(ccid = self.ccid, first_name = self.first_name, 
                                   last_name = self.last_name, email = self.email, ualberta_id = self.ualberta_id)
        
    def test_get_coordinator(self):
        obj = Coordinator.objects.get(ccid = self.ccid)
        
        self.assertEqual(obj.ccid, self.ccid)
        self.assertEqual(obj.first_name, self.first_name)
        self.assertEqual(obj.last_name, self.last_name)
        self.assertEqual(obj.email, self.email)
        self.assertEqual(obj.ualberta_id, self.ualberta_id)
    
    def test_create_duplicate_coordinator(self):  
        with self.assertRaises(IntegrityError):
            Coordinator.objects.create(ccid = self.ccid)
        with self.assertRaises(IntegrityError):
            Coordinator.objects.create(ualberta_id = self.ualberta_id)        
            
    def test_user_model_is_created_with_coordinator(self):
        obj = Coordinator.objects.get(ccid = self.ccid)
        user = obj.user
        self.assertEqual(user.username, obj.ccid)
        
    def test_user_model_is_correct_for_coordinator(self):
        obj = Coordinator.objects.get(ccid = self.ccid)
        user = obj.user
        user2 = User.objects.get(username = self.ccid)
        self.assertEqual(user, user2)
        
    def test_delete_coordinator(self):
        obj = Coordinator.objects.get(ccid = self.ccid)
        ccid = obj.ccid
        self.assertIsNotNone(obj)
        user = User.objects.get(username = self.ccid)
        self.assertIsNotNone(user)
        obj.delete()
        with self.assertRaises(Coordinator.DoesNotExist):
            obj = Coordinator.objects.get(ccid = self.ccid)
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username = self.ccid)


class StudentModelTests(TestCase):
    
    def setUp(self):
        
        self.ccid = "Student"
        self.first_name = "A"
        self.last_name = "Student"
        self.email = "aStudent@test.com"
        self.ualberta_id = 1
        self.programcode = "SP"
        self.programname = "StudentProgram"
        self.yearname = "StudentYear"
        
        program = Program.objects.create(code = self.programcode, name = self.programname)
        year = YearOfStudy.objects.create(year = self.yearname)
        
        Student.objects.create(ccid = self.ccid, first_name = self.first_name, last_name = self.last_name, 
                               email = self.email, ualberta_id = self.ualberta_id, year = year, program = program)        
        
        
    def test_get_student(self):
        obj = Student.objects.get(ccid = self.ccid)
        program = Program.objects.get(code = self.programcode)
        year = YearOfStudy.objects.get(year = self.yearname)
        
        self.assertEqual(obj.ccid, self.ccid)
        self.assertEqual(obj.first_name, self.first_name)
        self.assertEqual(obj.last_name, self.last_name)
        self.assertEqual(obj.email, self.email)
        self.assertEqual(obj.ualberta_id, self.ualberta_id)
        self.assertEqual(obj.program, program)
        self.assertEqual(obj.year, year)
        
    def test_create_duplicate_student(self):  
        with self.assertRaises(IntegrityError):
            Student.objects.create(ccid = self.ccid)
        with self.assertRaises(IntegrityError):
            Student.objects.create(ualberta_id = self.ualberta_id)               
        
    def test_user_model_is_created_with_student(self):
        obj = Student.objects.get(ccid = self.ccid)
        user = obj.user
        self.assertEqual(user.username, obj.ccid)    
        
    def test_user_model_is_correct_for_student(self):
        obj = Student.objects.get(ccid = self.ccid)
        user = obj.user
        user2 = User.objects.get(username = self.ccid)
        self.assertEqual(user, user2)    
        
    def test_program_delete(self):
        
        Program.objects.get(code = self.programcode).delete()
        
        student = Student.objects.get(ccid = self.ccid)  
        self.assertIsNone(student.program)
        
    
    def test_year_delete(self):
        
        with self.assertRaises(ProtectedError):
            YearOfStudy.objects.get(year = "StudentYear").delete()
            
            
    def test_delete_coordinator(self):
        obj = Student.objects.get(ccid = self.ccid)
        ccid = obj.ccid
        self.assertIsNotNone(obj)
        user = User.objects.get(username = self.ccid)
        self.assertIsNotNone(user)
        obj.delete()
        with self.assertRaises(Student.DoesNotExist):
            obj = Student.objects.get(ccid = self.ccid)
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username = self.ccid)    
            
