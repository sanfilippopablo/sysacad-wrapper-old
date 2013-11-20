$(document).ready(function() {
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });
});

$('.loading-new-data').tooltip()

$('#notificaciones').popover()