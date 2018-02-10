from django.db import models
from django.contrib.auth.models import User

class Student(User):
    ccid = models.CharField(max_length=8)
    
    def get_ccid(self):
        return self.ccid