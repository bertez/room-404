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
	},
	shuffle: function(o) { //http://dzone.com/snippets/array-shuffle-javascript
		for (var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
		return o;
	}
};
