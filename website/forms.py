 # -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from django.contrib.auth import authenticate
from sysacad_wrapper.settings import FR
from website.auth import SysacadSession

class PasswordOnlyForm(forms.Form):
	password = forms.CharField(
		required = True,
		label = u'Contraseña',
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

class AjustesPersonalesForm(forms.Form):
	email = forms.EmailField(
		required = False,
		label = 'Email',
	)
	old_password = forms.CharField(
		required = False,
		label = u'Contraseña anterior',
		widget = forms.PasswordInput,
	)

	new_password1 = forms.CharField(
		required = False,
		label = u'Nueva contraseña',
		widget = forms.PasswordInput,
	)
	new_password2 = forms.CharField(
		required = False,
		label = u'Repetir nueva contraseña',
		widget = forms.PasswordInput,
	)

	def __init__(self, user, *args, **kwargs):
		super(AjustesPersonalesForm, self).__init__(*args, **kwargs)
		self.user = user
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_action = '.'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-4'
		self.helper.field_class = 'col-lg-4'
		self.helper.layout = layout.Layout(
			layout.Fieldset(
				'Email',
				'email',
			),
			layout.Fieldset(
				u'Contraseña',
				'old_password',
				'new_password1',
				'new_password2',
			),
			layout.Submit('submit', 'Guardar')
		)

	def clean_old_password(self):
		old_password = self.cleaned_data.get('old_password')
		if old_password != "":
			if authenticate(fr=self.user.fr, legajo=self.user.legajo, password=old_password) is None:
				raise forms.ValidationError('La contraseña anterior es incorrecta.')
		else:
			password1 = self.cleaned_data.get('new_password1')
			password2 = self.cleaned_data.get('new_password2')
			if password1 or password2:
				raise ValidationError('Debes introducir tu contraseña anterior.')
		return old_password

	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		if password1 or password2:
			if password1 != password2:
				raise forms.ValidationError('Las contraseñas no coinciden.')
		return password2

	def clean(self):
		old_password = self.cleaned_data.get('old_password')
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		print old_password, password1, password2
		if old_password and password1:
			if old_password == password1:
				raise forms.ValidationError('La nueva contraseña debe ser distinta a la anterior.')
		return self.cleaned_data

	def save(self, commit=True):
		s = SysacadSession(base_url=FR[self.user.fr]['base_url'], alumno=self.user)
		s.change_password(self.cleaned_data['old_password'], self.cleaned_data['new_password1'])
		self.user.set_password(self.cleaned_data['new_password1'])
		if self.cleaned_data['email'] != "":
			self.user.email = self.cleaned_data['email']
		if commit:
			self.user.save()
		return self.user