from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from ..models import Adjudicator, Coordinator, Student, Program, YearOfStudy, Award, Application, Committee, Comment, Ranking
from django.db.models.deletion import ProtectedError
import datetime
import pytz

class AdjudicatorModelTests(TestCase):

    def setUp(self):
        self.ccid = "Adjudicator"
        self.first_name = "An"
        self.last_name = "Adjudicator"
        self.email = "anAdjudicator@test.com"
        Adjudicator.objects.create(ccid = self.ccid, first_name = self.first_name,
                                   last_name = self.last_name, email = self.email)

    def test_get_adjudicator(self):
        obj = Adjudicator.objects.get(ccid = self.ccid)

        self.assertEqual(obj.ccid, self.ccid)
        self.assertEqual(obj.first_name, self.first_name)
        self.assertEqual(obj.last_name, self.last_name)
        self.assertEqual(obj.email, self.email)

    def test_create_duplicate_adjudicator(self):
        with self.assertRaises(IntegrityError):
            Adjudicator.objects.create(ccid = self.ccid)

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
        Coordinator.objects.create(ccid = self.ccid, first_name = self.first_name,
                                   last_name = self.last_name, email = self.email)

    def test_get_coordinator(self):
        obj = Coordinator.objects.get(ccid = self.ccid)

        self.assertEqual(obj.ccid, self.ccid)
        self.assertEqual(obj.first_name, self.first_name)
        self.assertEqual(obj.last_name, self.last_name)
        self.assertEqual(obj.email, self.email)

    def test_create_duplicate_coordinator(self):
        with self.assertRaises(IntegrityError):
            Coordinator.objects.create(ccid = self.ccid)

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
        self.student_id = '1'
        self.programcode = "SP"
        self.programname = "StudentProgram"
        self.yearname = "StudentYear"
        
        program = Program.objects.create(code = self.programcode, name = self.programname)
        year = YearOfStudy.objects.create(year = self.yearname)
        
        Student.objects.create(ccid = self.ccid, first_name = self.first_name, last_name = self.last_name, 
                               email = self.email, student_id = self.student_id, year = year, program = program)        
        
        
    def test_get_student(self):
        obj = Student.objects.get(ccid = self.ccid)
        program = Program.objects.get(code = self.programcode)
        year = YearOfStudy.objects.get(year = self.yearname)
        
        self.assertEqual(obj.ccid, self.ccid)
        self.assertEqual(obj.first_name, self.first_name)
        self.assertEqual(obj.last_name, self.last_name)
        self.assertEqual(obj.email, self.email)
        self.assertEqual(obj.student_id, self.student_id)
        self.assertEqual(obj.program, program)
        self.assertEqual(obj.year, year)
        
    def test_create_duplicate_student(self):  
        with self.assertRaises(IntegrityError):
            Student.objects.create(ccid = self.ccid)
        with self.assertRaises(IntegrityError):
            Student.objects.create(student_id = self.student_id)               
        
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
            
    def test_delete_student(self):
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
            

class ApplicationTestModels(TestCase):
    
    def setUp(self):
        self.ccid = "Student"
        self.first_name = "A"
        self.last_name = "Student"
        self.email = "aStudent@test.com"
        self.student_id = '1'
        self.year = "First"
        self.year_of_study = YearOfStudy.objects.create(year = self.year)
        self.program_code = "PRFG"
        self.program_name = "Science"
        self.program = Program.objects.create(code = self.program_code, name = self.program_name)
        self.award_name = "This award"
        self.award_description = "For students"
        self.award_value = "One gold pen"
        self.award_start_date = str(datetime.datetime.now(pytz.timezone('America/Vancouver')))
        self.award_end_date = str(datetime.datetime.now(pytz.timezone('America/Edmonton')))
        self.award_documents_needed = False
        self.award_is_active = True
        self.award = Award.objects.create(award_name = self.award_name, description = self.award_description, value = self.award_value,
                                          start_date = self.award_start_date, end_date = self.award_end_date, 
                                          documents_needed = self.award_documents_needed, is_active = self.award_is_active)
        self.award.programs.add(self.program)
        self.award.years_of_study.add(self.year_of_study)
        self.student = Student.objects.create(ccid = self.ccid, first_name = self.first_name, last_name = self.last_name,
                                              email = self.email, student_id = self.student_id, year = self.year_of_study, program = self.program)
        self.application_is_submitted = False
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
            
    def test_submit_application(self):
        self.application.is_submitted = True
        self.application.save()
        application = Application.objects.get(application_id = self.application.application_id)
        self.assertTrue(application.is_submitted)
        self.application.is_submitted = False
        self.application.save()
        application = Application.objects.get(application_id = self.application.application_id)
        self.assertFalse(application.is_submitted)
     
        
class ProgramModelTests(TestCase):
    
    def setUp(self):
        self.ccid = "Student"
        self.first_name = "A"
        self.last_name = "Student"
        self.email = "aStudent@test.com"
        self.student_id = '1'
        self.year = "First"
        self.year_of_study = YearOfStudy.objects.create(year = self.year)
        self.program_code = "PRFG"
        self.program_name = "Science"
        self.program = Program.objects.create(code = self.program_code, name = self.program_name)
        self.award_name = "This award"
        self.award_description = "For students"
        self.award_value = "One gold pen"
        self.award_start_date = str(datetime.datetime.now(pytz.timezone('America/Vancouver')))
        self.award_end_date = str(datetime.datetime.now(pytz.timezone('America/Edmonton')))
        self.award_documents_needed = False
        self.award_is_active = True
        self.award = Award.objects.create(award_name = self.award_name, description = self.award_description, value = self.award_value,
                                          start_date = self.award_start_date, end_date = self.award_end_date,
                                          documents_needed = self.award_documents_needed, is_active = self.award_is_active)
        self.award.programs.add(self.program)
        self.award.years_of_study.add(self.year_of_study)        
        self.student = Student.objects.create(ccid = self.ccid, first_name = self.first_name, last_name = self.last_name,
                                              email = self.email, student_id = self.student_id, year = self.year_of_study, program = self.program)        
    
    def test_program_creation(self):
        program = Program.objects.get(code = self.program_code)
        self.assertIsNotNone(program)
        
    def test_program_duplicate(self):
        with self.assertRaises(IntegrityError):
            new_program = Program.objects.create(code = self.program_code)
            
    def test_program_deletion_cascade(self):
        award = Award.objects.get(awardid = self.award.awardid)
        student = Student.objects.get(ccid = self.ccid)
        program = Program.objects.get(code = self.program_code)
        self.assertEqual(student.program, program)
        self.assertTrue(program in award.programs.all())
        program.delete()
        award = Award.objects.get(awardid = self.award.awardid)
        student = Student.objects.get(ccid = self.ccid)
        self.assertIsNone(student.program)
        self.assertFalse(program in award.programs.all())
        

class AwardModelTests(TestCase):
    def setUp(self):
        self.award_name = "Award Name 1"
        self.description = "Award Description 1"
        self.value = "Award Value 1"
        self.start_date = str(datetime.datetime.now(pytz.timezone('America/Vancouver')))
        self.end_date = str(datetime.datetime.now(pytz.timezone('America/Edmonton')))
        self.programcode = "AP"
        self.programname = "AwardProgram"
        self.yearname = "AwardYear"
        self.documents_needed = False
        self.is_active = True 
        self.year = YearOfStudy.objects.create(year = self.yearname)
        self.program = Program.objects.create(code = self.programcode, name = self.programname)
        self.award = Award.objects.create(award_name = self.award_name, description = self.description, value = self.value,
                                    start_date = self.start_date, end_date = self.end_date, 
                                    documents_needed = self.documents_needed, is_active = self.is_active)
        self.award.programs.add(self.program)
        self.award.years_of_study.add(self.year)

    def test_award_creation(self):
        award = Award.objects.get(awardid = self.award.awardid)
        self.assertIsNotNone(award)

    def test_award_duplicate(self):
        with self.assertRaises(IntegrityError):
            new_award = Award.objects.create(awardid = self.award.awardid)

class CommitteeModelTests(TestCase):
    def setUp(self):
        self.committee_name = "Committee Name 1"
        self.adjudicator_ccid = "Committee Adjudicator 1"
        self.adjudicator_first_name = "Adjudicator 1 First"
        self.adjudicator_last_name = "Adjudicator 1 Last"
        self.adjudicator_email = "Adjudicator1@test.com"
        self.adjudicator = Adjudicator.objects.create(ccid = self.adjudicator_ccid, first_name = self.adjudicator_first_name,
                                   last_name = self.adjudicator_last_name, email = self.adjudicator_email)
        self.award_name = "Award Name 1"
        self.description = "Award Description 1"
        self.value = "Award Value 1"
        self.start_date = str(datetime.datetime.now(pytz.timezone('America/Vancouver')))
        self.end_date = str(datetime.datetime.now(pytz.timezone('America/Edmonton')))
        self.programcode = "AP"
        self.programname = "AwardProgram"
        self.yearname = "AwardYear"
        self.documents_needed = False
        self.is_active = True 
        self.year = YearOfStudy.objects.create(year = self.yearname)
        self.program = Program.objects.create(code = self.programcode, name = self.programname)

        self.award = Award.objects.create(award_name = self.award_name, description = self.description, value = self.value,
                                    start_date = self.start_date, end_date = self.end_date, 
                                    documents_needed = self.documents_needed, is_active = self.is_active)
        self.award.programs.add(self.program)
        self.award.years_of_study.add(self.year)
        self.committee = Committee.objects.create(committee_name = self.committee_name)
        self.committee.adjudicators.add(self.adjudicator)
        self.committee.awards.add(self.award)

    def test_committee_creation(self):
        committee = Committee.objects.get(committeeid = self.committee.committeeid)
        self.assertIsNotNone(committee)

    def test_committee_duplicate(self):
        with self.assertRaises(IntegrityError):
            new_committee = Committee.objects.create(committeeid = self.committee.committeeid)


class CommentTestModels(TestCase):
    
    def setUp(self):
        self.ccid = "Student"
        self.first_name = "A"
        self.last_name = "Student"
        self.email = "aStudent@test.com"
        self.student_id = '1'
        self.year = "First"
        self.year_of_study = YearOfStudy.objects.create(year = self.year)
        self.program_code = "PRFG"
        self.program_name = "Science"
        self.program = Program.objects.create(code = self.program_code, name = self.program_name)
        self.award_name = "This award"
        self.award_description = "For students"
        self.award_value = "One gold pen"
        self.award_start_date = str(datetime.datetime.now(pytz.timezone('America/Vancouver')))
        self.award_end_date = str(datetime.datetime.now(pytz.timezone('America/Edmonton')))
        self.award_documents_needed = False
        self.award_is_active = True
        self.award = Award.objects.create(award_name = self.award_name, description = self.award_description, value = self.award_value,
                                          start_date = self.award_start_date, end_date = self.award_end_date, 
                                          documents_needed = self.award_documents_needed, is_active = self.award_is_active)
        self.award.programs.add(self.program)
        self.award.years_of_study.add(self.year_of_study)
        self.student = Student.objects.create(ccid = self.ccid, first_name = self.first_name, last_name = self.last_name,
                                              email = self.email, student_id = self.student_id, year = self.year_of_study, program = self.program)
        self.application_is_submitted = False
        self.application = Application.objects.create(award = self.award, student = self.student, is_submitted = self.application_is_submitted)
        self.adjudicator_ccid = "Committee Adjudicator 1"
        self.adjudicator_first_name = "Adjudicator 1 First"
        self.adjudicator_last_name = "Adjudicator 1 Last"
        self.adjudicator_email = "Adjudicator1@test.com"
        self.adjudicator = Adjudicator.objects.create(ccid = self.adjudicator_ccid, first_name = self.adjudicator_first_name,
                                   last_name = self.adjudicator_last_name, email = self.adjudicator_email)
        self.comment_text = "Hello World"
        self.comment = Comment.objects.create(application = self.application, adjudicator = self.adjudicator, comment_text = self.comment_text)

    def test_get_comment(self):
        obj = Comment.objects.get(comment_text = self.comment_text)
        application = Application.objects.get(application_id = self.application.application_id)
        adjudicator = Adjudicator.objects.get(ccid = self.adjudicator_ccid)
        
        self.assertEqual(obj.comment_text, self.comment_text)
        self.assertEqual(obj.application, self.application)
        self.assertEqual(obj.adjudicator, self.adjudicator)

class RankingTestModels(TestCase):
    
    def setUp(self):
        self.ccid = "Student"
        self.first_name = "A"
        self.last_name = "Student"
        self.email = "aStudent@test.com"
        self.student_id = '1'
        self.year = "First"
        self.year_of_study = YearOfStudy.objects.create(year = self.year)
        self.program_code = "PRFG"
        self.program_name = "Science"
        self.program = Program.objects.create(code = self.program_code, name = self.program_name)
        self.award_name = "This award"
        self.award_description = "For students"
        self.award_value = "One gold pen"
        self.award_start_date = str(datetime.datetime.now(pytz.timezone('America/Vancouver')))
        self.award_end_date = str(datetime.datetime.now(pytz.timezone('America/Edmonton')))
        self.award_documents_needed = False
        self.award_is_active = True
        self.award = Award.objects.create(award_name = self.award_name, description = self.award_description, value = self.award_value,
                                          start_date = self.award_start_date, end_date = self.award_end_date, 
                                          documents_needed = self.award_documents_needed, is_active = self.award_is_active)
        self.award.programs.add(self.program)
        self.award.years_of_study.add(self.year_of_study)
        self.student = Student.objects.create(ccid = self.ccid, first_name = self.first_name, last_name = self.last_name,
                                              email = self.email, student_id = self.student_id, year = self.year_of_study, program = self.program)
        self.application_is_submitted = False
        self.application = Application.objects.create(award = self.award, student = self.student, is_submitted = self.application_is_submitted)
        self.adjudicator_ccid = "Committee Adjudicator 1"
        self.adjudicator_first_name = "Adjudicator 1 First"
        self.adjudicator_last_name = "Adjudicator 1 Last"
        self.adjudicator_email = "Adjudicator1@test.com"
        self.adjudicator = Adjudicator.objects.create(ccid = self.adjudicator_ccid, first_name = self.adjudicator_first_name,
                                   last_name = self.adjudicator_last_name, email = self.adjudicator_email)
        self.rank = 2
        self.ranking = Ranking.objects.create(award = self.award, application = self.application, adjudicator = self.adjudicator, rank = self.rank)


    def test_get_ranking(self):
        obj = Ranking.objects.get(award = self.award)
        application = Application.objects.get(application_id = self.application.application_id)
        adjudicator = Adjudicator.objects.get(ccid = self.adjudicator_ccid)
        award = Award.objects.get(awardid = self.award.awardid)
        
        self.assertEqual(obj.rank, self.rank)
        self.assertEqual(obj.application, self.application)
        self.assertEqual(obj.adjudicator, self.adjudicator)
        self.assertEqual(obj.award, self.award)