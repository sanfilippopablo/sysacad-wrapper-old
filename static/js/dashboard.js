var loadNewDashboardData = function () {
	$.ajax({
	    url : '/ajax/dashboard_data/',
	    type: 'POST',
	    headers: SysacadWrapper.djangoHeaders(),
	    success : function(data) {
	        if (data['state'] == 'password_required') {
	        	SysacadWrapper.requestPassword();
	        	SysacadWrapper.callWhenSessionReady(loadNewDashboardData);
	        } else {
	        	$('#content-container').html(data['html']);
	        	$('.actualizando-alert').removeClass('active');
	        };
	    }
	});
}
$(document).ready(function(){
	loadNewDashboardData();
})
