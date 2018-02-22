from django.forms import *from django.utils.translation import gettext_lazy as _from .models_FSJUser import FSJUserfrom .forms_student import *from .forms_adjudicator import *from .forms_coordinator import *from .forms_award import *class ProfileForm(forms.Form):       ccid = CharField(label = _("ccid"), max_length = 255)       first_name = CharField(label = _("First Name"), max_length = 255)       last_name = CharField(label = _("Last Name"), max_length = 255)       email = EmailField(label = _("Email"))       lang_pref = ChoiceField(label = _("Language Preference"), choices = FSJUser.LANG_CHOICES)              def __init__(self, *args, **kwargs):              super(ProfileForm, self).__init__(*args, **kwargs)                         self.fields['ccid'].disabled = True              self.fields['email'].disabled = True        