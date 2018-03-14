from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from ..models import Adjudicator, Coordinator


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