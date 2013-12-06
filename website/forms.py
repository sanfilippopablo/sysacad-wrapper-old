 # -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from django.contrib.auth import authenticate
from sysacad_wrapper.settings import FR
from website.auth import SysacadSession

class RenewSysacadSessionForm(forms.Form):
	password = forms.CharField(
		required = True,
		label = u'Contraseña',
		widget = forms.PasswordInput,
	)

	def __init__(self, user=None, *args, **kwargs):
		super(RenewSysacadSessionForm, self).__init__(*args, **kwargs)
		self.user = user
		self.helper = FormHelper()
		self.helper.form_class = 'renew-sysacad-session-form'
		self.helper.form_method = 'post'
		self.helper.layout = layout.Layout(
			layout.HTML(
				u"""
				<div class="modal fade password-required-modal" data-show="false">
				  <div class="modal-dialog">
				    <div class="modal-content">
				      <div class="modal-header">
				        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
				        <h4 class="modal-title">Contraseña requerida</h4>
				      </div>
				      <div class="modal-body clearfix">
				        <p>La sesión de Sysacad expiró. Necesitamos tu contraseña para poder recuperar los datos.</p>
				        <div class="col-lg-6 col-lg-offset-3 col-md-8 col-md-offset-2 col-sm-10 col-sm-offset-1 form-group">
				"""
			),
			layout.Field('password', placeholder="Contraseña"),
			layout.HTML(
				"""
				        </div>
				      </div>
				      <div class="modal-footer">
				        <button type="button" class="btn btn-default" data-dismiss="modal">Salir</button>
				        <button type="submit" class="btn btn-primary submit-button">Enviar</button>
				      </div>
				    </div><!-- /.modal-content -->
				  </div><!-- /.modal-dialog -->
				</div><!-- /.modal -->
				<style>
				.asteriskField {
				    display: none;
				}
				</style>
				"""
			)
		)

	def clean_password(self):
		password = self.cleaned_data.get('password')
		print password
		if authenticate(fr=self.user.fr, legajo=self.user.legajo, password=password) is None:
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
		sysacad = SysacadSession(alumno=self.user)
		sysacad.change_password(self.cleaned_data['old_password'], self.cleaned_data['new_password1'])
		sysacad.close()
		self.user.set_password(self.cleaned_data['new_password1'])
		if self.cleaned_data['email'] != "":
			self.user.email = self.cleaned_data['email']
		if commit:
			self.user.save()
		return self.user