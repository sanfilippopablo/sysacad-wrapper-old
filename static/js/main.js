$(document).ready(function() {
	// Off-Canvas
 	$('[data-toggle=offcanvas]').click(function() {
    	$('.row-offcanvas').toggleClass('active');
  	});

});

SysacadWrapper = {
	callbacksPending: [],
	// getCookkie(name): returns cookie value from cookie name.
	getCookie: function(name) {
  		var parts = document.cookie.split(name + "=");
  		if (parts.length == 2) return parts.pop().split(";").shift();
	},

	djangoHeaders: function() {
		return {
			'X-CSRFToken': this.getCookie('csrftoken'),
	    	'sessionid': this.getCookie('sessionid')
	    }
	},

	requestPassword: function() {
		sObject = this;
		$('.password-required-modal').modal('show');
		$(document).on('submit', '.renew-sysacad-session-form', function (e) {
			e.preventDefault();
			$('.password-required-modal').modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
			$.ajax({
				url: '/ajax/renew-sysacad-session/',
				type: 'POST',
				headers: sObject.djangoHeaders(),
				data: $('.renew-sysacad-session-form').serialize(),
				success: function (data) {
					if (data['valid']) {
						sObject.callPendingCallbacks();
					} else {
						// Render form.
						$('.renew-sysacad-session-form').replaceWith(data['form_html']);
						$('.password-required-modal').modal('show')

					}
				}
			})
		})
	},

	callWhenSessionReady: function(callback) {
		this.callbacksPending.push(callback);
	},

	callPendingCallbacks: function() {
		for (var i = this.callbacksPending.length - 1; i >= 0; i--) {
			var cb = this.callbacksPending.pop();
			cb();
		};
	}
};