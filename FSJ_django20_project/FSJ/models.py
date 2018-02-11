from django.db import models

class FSJUser(models.Model):
    username = models.CharField(max_length=100)
    ccid = models.CharField(max_length=8)
    
    def __str__(self):
        return self.username
    
    @property
    def user_class(self):
        return "hi"    
    
    def get_ccid(self):
        return self.ccid
    
    def get_username(self):
        return self.username
    
class Student(FSJUser):
    program = models.CharField(max_length=50)

    def user_class(self):
        return "Student"
            
    def get_program(self):
        return self.program
    
class Coordinator(FSJUser):
    def user_class(self):
        return "Coordinator"
    
class Adjudicator(FSJUser):
    def user_class(self):
        return "Adjudicator"
    
    

    