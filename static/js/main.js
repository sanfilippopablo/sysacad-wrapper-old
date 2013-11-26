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
		console.log("Password required. Launching modal.")
		sObject = this;
		var $passwordRequiredModal = $('.password-required-modal');
		$passwordRequiredModal.modal('show');
		$passwordRequiredModal.on('click', '.submit-button', function (e) {
			$('.password-required-modal .modal-body *').hide();
			$('.password-required-modal .modal-body').append('<img src="static/img/big-ajax-loader.gif" alt="Cargando" class="loading-img"/>');
			$.ajax({
				url: '/ajax/renew-sysacad-session/',
				type: 'POST',
				headers: sObject.djangoHeaders(),
				data: $('.renew-sysacad-session-form').serialize(),
				success: function (data) {
					if (data['valid']) {
						// Ocultar modal.
						$passwordRequiredModal.modal('hide');
						sObject.callPendingCallbacks();
					} else {
						// Render form inside modal.
						$('.password-required-modal .form').replaceWith(data['form_html']);
						$('.password-required-modal .loading-img').remove();
						$('.password-required-modal .modal-body *').show();

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