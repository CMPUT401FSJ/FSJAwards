from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from ..models import Adjudicator, Coordinator, Student, Program, YearOfStudy, Award, Application
from django.db.models.deletion import ProtectedError
import datetime
import pytz

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
        # Link FSJUser with a User model for authentication related business
        user = User.objects.create(username = "TestStudent", password = "studentpassword")
        program = Program.objects.create(code = "SP", name = "StudentProgram")
        year = YearOfStudy.objects.create(year = "StudentYear")
        student = Student.objects.create(user = user, ccid = "TestStudent", first_name = "A",
                                         last_name = "Student", email = "astudent@test.com", ualberta_id = 1,
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


class ApplicationTestModels(TestCase):
    
    def setUp(self):
        self.ccid = "Student"
        self.first_name = "A"
        self.last_name = "Student"
        self.email = "aStudent@test.com"
        self.ualberta_id = 1
        self.year = "First"
        self.year_of_study = YearOfStudy.objects.create(year = self.year)
        self.program_code = "PRFG"
        self.program_name = "Science"
        self.program = Program.objects.create(code = self.program_code, name = self.program_name)
        self.award_name = "This award"
        self.award_description = "For students"
        self.award_value = "One gold pen"
        self.award_deadline = str(datetime.datetime.now(pytz.timezone('America/Edmonton')))
        self.award_documents_needed = False
        self.award_is_active = True
        self.award = Award.objects.create(award_name = self.award_name, description = self.award_description, value = self.award_value,
                                          deadline = self.award_deadline,
                                          documents_needed = self.award_documents_needed, is_active = self.award_is_active)
        self.award.programs.add(self.program)
        self.award.years_of_study.add(self.year_of_study)
        self.student = Student.objects.create(ccid = self.ccid, first_name = self.first_name, last_name = self.last_name,
                                              email = self.email, ualberta_id = self.ualberta_id, year = self.year_of_study, program = self.program)
        self.application_is_submitted = True
        self.application = Application.objects.create(award = self.award, student = self.student, is_submitted = self.application_is_submitted)

    def test_application_creation(self):
        application = Application.objects.get(application_id = self.application.application_id)
        self.assertEqual(application, self.application)
        self.assertEqual(application.application_id, self.application.application_id)
        self.assertEqual(application.award, self.application.award)
        self.assertEqual(application.student.ccid, self.application.student.ccid)
        self.assertEqual(application.is_submitted, self.application.is_submitted)
        
    def test_application_duplicate(self):
        with self.assertRaises(IntegrityError):
            Application.objects.create(application_id = self.application.application_id)
            
    
    def test_application_delete_award(self):
        Award.objects.get(awardid = self.award.awardid).delete()
        with self.assertRaises(Application.DoesNotExist):
            application = Application.objects.get(application_id = self.application.application_id)
            
    def test_application_delete_student(self):
        Student.objects.get(ccid = self.ccid).delete()
        with self.assertRaises(Application.DoesNotExist):
            application = Application.objects.get(application_id = self.application.application_id)        
