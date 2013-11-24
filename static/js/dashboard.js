function getCookie(name) {
  var parts = document.cookie.split(name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

$(document).ready(function() {
	$.ajax({
	    url : '/ajax/dashboard_data/',
	    type: 'POST',
	    headers: {'X-CSRFToken':getCookie('csrftoken')
	        ,'sessionid':getCookie('sessionid')
	        },
	    success : function(data) {
	        if (data['state'] == 'password_required') {
	        	console.log('Password required.');
	        } else {
	        	$('#content-container').html(data['html']);
	        	$('.actualizando-alert').removeClass('active');
	        };
	    }
	});
});