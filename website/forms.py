 # -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth import authenticate
from sysacad_wrapper.settings import FR

class PasswordOnlyForm(forms.Form):
	password = forms.CharField(
		required = True,
		label = 'Contraseña',
		widget = forms.PasswordInput,
	)
	def __init__(self, *args, **kwargs):
		super(PasswordOnlyForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()

	def clean_password(self):
		password = self.cleaned_data['password']
		if authenticate(FR[self.user.fr]['base_url'], self.user.legajo, password) is None:
			raise ValidationError('La contraseña es incorrecta.')
		return password