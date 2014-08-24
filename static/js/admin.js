/* global $, helpers */

var $log = $('#log');

$('button').on('click', function(e) {
	var payload = {
		id: $(this).data('id')
	};

	if(confirm('Are you sure? there is no UNDO.')) {
		helpers.request('POST', '', payload, function(response) {

			location.reload();

		});
	}


	e.preventDefault();
});
