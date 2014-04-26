(function($) {
	var $intro = $('#intro');
	var $a = $('#scene-a');
	var $b = $('#scene-b');
	var $c = $('#scene-c');
	var $d = $('#scene-d');
	var $category_list = $('#categories');

	var available_categories; 
	var chosen_categories;

	$.get('/categories', function(d) {
		//create the initial category list
		$.each(d, function(id, category) {
			$('<div>').html(category)
			.data('category', {id: category})
			.data('category', {id: category})
			.appendTo($category_list);
		});

		$intro.fadeOut('fast', function() {
			$a.fadeIn();
			scene_a();
		});

	});
	
	// Choose from different categories
	function scene_a(){
		var all_categories = $category_list.find('div');
		all_categories.on('click', function(e){
			var chosen = $(this).data('chosen');
			if(chosen) {
				$(this).data('chosen', false);
			
			} else {
				$(this).data('chosen', true);
			
			}
			buildChosen();
			e.preventDefault();
		});

		function buildChosen() {
			$.each(all_categories, function(c) {
			
			});
		
		}

		

	
	}
	
})(jQuery);
