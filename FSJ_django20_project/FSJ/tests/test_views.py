from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from ..views import profile
from ..models import Student, YearOfStudy

class ProfileViewTests(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.username = "JOE"
        self.email = "Joe@Joe.ca"
        self.password = "myPass!"
        self.url = '/FSJ/profile'
        self.user = User.objects.create_user(username = self.username, email = self.email, password = self.password)
        self.ccid = "Student"
        self.first_name = "A"
        self.last_name = "Student"
        self.email = "aStudent@test.com"
        self.student_id = '1'
        self.year = "First"
        self.year_of_study = YearOfStudy.objects.create(year = self.year)
        self.student = Student.objects.create(ccid = self.ccid, first_name = self.first_name, 
                                   last_name = self.last_name, email = self.email, student_id = self.student_id, year = self.year_of_study)
        
    def test_not_logged_in(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        response = profile(request)
        # redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=' + self.url)
        
    def test_get_logged_in_without_FSJ_user(self):
        request = self.factory.get(self.url)
        request.user = self.user
        self.assertEqual(request.method, "GET")
        # User without corresponding FSJ User gets permission denied due to decorator
        with self.assertRaises(PermissionDenied):
            response = profile(request)
            
    def test_post_logged_in_without_FSJ_user(self):
        request = self.factory.post(self.url)
        request.user = self.user
        self.assertEqual(request.method, "POST")
        # User without corresponding FSJ User gets permission denied due to decorator
        with self.assertRaises(PermissionDenied):
            response = profile(request)            
        
    def test_get_logged_in_with_Student(self):
        request = self.factory.get(self.url)
        request.user = self.student.user
        self.assertEqual(request.method, "GET")
        response = profile(request)
        self.assertEqual(response.status_code, 200)
        
    def test_post_logged_in_with_Student(self):
        request = self.factory.post(self.url)
        request.user = self.student.user
        self.assertEqual(request.method, "POST")
        response = profile(request)
        self.assertEqual(response.status_code, 200)    