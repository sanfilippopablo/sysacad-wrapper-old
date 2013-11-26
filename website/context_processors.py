from website.forms import RenewSysacadSessionForm

def renew_sysacad_session_form(request):
	return {'renew_sysacad_session_form': RenewSysacadSessionForm() }