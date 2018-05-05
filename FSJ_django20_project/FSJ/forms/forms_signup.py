from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django import forms

class SignupForm(forms.Form):
	email = forms.EmailField(max_length=200)

	def clean(self):
		cleaned_data = super(SignupForm, self).clean()
		email = cleaned_data.get('email')
		if not email:
			raise forms.ValidationError(_('An email is required'))

