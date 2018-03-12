from django.core.exceptions import PermissionDenied
from .models import *

# Generic utility method to ensure a user is an FSJUser (specifically, one of the accepted children user types of the parent FSJUser) to control access
def is_FSJ_user(usr):
    user = get_FSJ_user(usr)
    if not isinstance(user, Student) and not isinstance(user, Adjudicator) and not isinstance(user, Coordinator):
        raise PermissionDenied
    return True

# Generic utility method to obtain the FSJUser model give a specific username from the User model (which matches the FSJUser's CCID)
# Returns None if there are no Students, Coordinators, or Adjudicators with that CCID
def get_FSJ_user(usr):
    FSJ_user = None
    try:
        FSJ_user = Student.objects.get(ccid=usr)
    except Student.DoesNotExist:
        try:
            FSJ_user = Adjudicator.objects.get(ccid=usr)
        except Adjudicator.DoesNotExist:
            try:
                FSJ_user = Coordinator.objects.get(ccid=usr)
            except Coordinator.DoesNotExist:
                pass
    return FSJ_user

# Generic utility method to obtain a context for template rendering which is contains any common required fields
def get_standard_context(usr):
    context = dict()
    context['FSJ_user'] = usr
    return context