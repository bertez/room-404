var helpers = {
	percent: function(count, total) {
		return Math.round((count * 100) / total);
	},
	request: function(url, data, fn) {
			$.ajax({
				method: 'POST',
				url: url,
				data: JSON.stringify(data),
				contentType: 'application/json',
				success: fn,
				error: function(response){
					//handle this
				}
			});
	}
};
