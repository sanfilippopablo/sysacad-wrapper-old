from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from sysacad_api import SysacadSession
from django.contrib.auth.decorators import login_required
from sysacad_wrapper.settings import FR
from django.utils import timezone
from datetime import timedelta, datetime

@login_required
def dashboard(request):
	materias = request.user.materias.filter(estado='cursa')
	return render_to_response('dashboard.html', RequestContext(request, {'materias': materias}))

@login_required
def dashboard_data(request):
	print datetime.now()
	print request.user.cookies.last_access
	valid_cookie = (timezone.now() - request.user.cookies.last_access) < timedelta(seconds=200)
	if valid_cookie:
		cookies = {request.user.cookies.key: request.user.cookies.value}
		s = SysacadSession(FR[request.user.fr]['base_url'], cookies=cookies)
	else:
		if request.POST.get('password'):
			s = SysacadSession(FR[request.user.fr]['base_url'])
			s.login(request.user.legajo, request.POST.get('password'))
		else:
			return HttpResponse('password_needed')

	materias_dict = s.allDataFromEstadoAcademico()['materias']
	materias = request.user.actualizar_materias(materias_dict).filter(estado='cursa')

	return render_to_response('dashboard_data.html', RequestContext(request, {'materias': materias}))