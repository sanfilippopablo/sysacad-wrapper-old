 # -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django.contrib.auth import authenticate
from sysacad_wrapper.settings import FR
from website.auth import SysacadSession

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
			raise forms.ValidationError('La contraseña es incorrecta.')
		return password

class ChangePasswordForm(forms.Form):
	old_password = forms.CharField(
		required = True,
		label = 'Contraseña anterior',
		widget = forms.PasswordInput,
	)

	new_password1 = forms.CharField(
		required = True,
		label = 'Nueva contraseña',
		widget = forms.PasswordInput,
	)
	new_password2 = forms.CharField(
		required = True,
		label = 'Repetir nueva contraseña',
		widget = forms.PasswordInput,
	)

	def __init__(self, user, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)
		self.user = user
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_action = '.'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-4'
		self.helper.field_class = 'col-lg-4'
		self.helper.layout = Layout(
			'old_password',
			'new_password1',
			'new_password2',
			Submit('submit', 'Guardar')
		)

	def clean_old_password(self):
		old_password = self.cleaned_data.get('old_password')
		if authenticate(fr=self.user.fr, legajo=self.user.legajo, password=old_password) is None:
			raise forms.ValidationError('La contraseña anterior es incorrecta.')
		return old_password

	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		if password1 and password2:
			if password1 != password2:
				raise forms.ValidationError('Las contraseñas no coinciden.')
		return password2

	def clean(self):
		old_password = self.cleaned_data.get('old_password')
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		if old_password and password1:
			if old_password == password1:
				raise forms.ValidationError('La nueva contraseña debe ser distinta a la anterior.')
		return self.cleaned_data

	def save(self, commit=True):
		s = SysacadSession(base_url=FR[self.user.fr]['base_url'], alumno=self.user)
		s.change_password(self.cleaned_data['old_password'], self.cleaned_data['new_password1'])
		self.user.set_password(self.cleaned_data['new_password1'])
		if commit:
			self.user.save()
		return self.user