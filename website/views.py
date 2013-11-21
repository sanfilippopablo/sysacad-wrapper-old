from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from sysacad_api import SysacadSession
from django.contrib.auth.decorators import login_required
from sysacad_wrapper.settings import FR_BASE_URL
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard(request):
	if (timezone.now() - request.user.cookies.last_access) > timedelta(seconds=200):
		return HttpResponseRedirect('/login/')
	cookies = {request.user.cookies.key: request.user.cookies.value}
	s = SysacadSession(FR_BASE_URL[request.user.fr], cookies=cookies)
	materias = s.materiasEnCurso()
	return render_to_response('dashboard.html', RequestContext(request, {'materias': materias}))

