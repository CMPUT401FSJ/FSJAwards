from django.contrib import admin

from .models import *

# Allow the admin site to maintain students, coordinators, adjudicators
admin.site.register(Student)
admin.site.register(Coordinator)
admin.site.register(Adjudicator)
admin.site.register(Award)
