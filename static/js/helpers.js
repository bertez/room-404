var helpers = {
	percent: function(count, total) {
		return Math.round((count * 100) / total);
	},
	request: function(method, url, data, fn) {
			$.ajax({
				method: method,
				url: url,
				data: data ? JSON.stringify(data) : null,
				contentType: 'application/json',
				success: fn,
				error: function(response){
					//handle this
					console.log(response);

					$('<div>')
					.html('Sorry, something broke. Please reload the page to try again.')
					.addClass('error')
					.appendTo('body');
				}
			});
	},
	shuffle: function(o) { //http://dzone.com/snippets/array-shuffle-javascript
		for (var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
		return o;
	}
};
