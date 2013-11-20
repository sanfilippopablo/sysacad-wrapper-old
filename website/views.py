from django.shortcuts import render_to_response
from django.template import RequestContext
from sysacad_api import SysacadSession
from django.contrib.auth.decorators import login_required
from sysacad_wrapper.settings import FR_BASE_URL

@login_required
def dashboard(request):
	s = SysacadSession(FR_BASE_URL[request.user.fr], cookies={request.user.cookies.key: request.user.cookies.value})
	materias = s.materiasEnCurso()
	return render_to_response('dashboard.html', RequestContext(request, {'materias': materias}))

