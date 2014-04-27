//sorry for the quick and dirty code
(function($) {
	//elements
	var $intro = $('#intro');
	var $scene_a = $('#scene-a');
	var $scene_b = $('#scene-b');
	var $scene_c = $('#scene-c');
	var $scene_d = $('#scene-d');
	var $category_list = $('#categories');
	var $chosen_category_list = $('#chosen_categories');
	var $dropspot = $('#drop');
	var $form = $('#form');
	var $pad = $('#pad');
	var $mine = $('#mine');
	var $other = $('#other');
	var $enter = $('#enter');
	var $final_my = $('#my_confession');
	var $final_other = $('#other_confessions');

	// buttons
	var $goto_b = $('#goto-b');
	var $goto_c = $('#goto-c');
	var $better = $('#better');
	var $worse = $('#worse');
	var $go = $('#go');

	//form
	var $confession = $('#confession');
	var $score = $('#score');

	// data variables
	var total_confessions;
	var available_categories; 
	var chosen_categories = [];
	var final_category;
	var confession;

	// Initial setup
	$.get('/categories', function(d) {
		//create the initial category list
		total_confessions = d.confessions;

		$.each(d.categories, function(id, category) {
			$('<div>').html(category.name)
			.data('category', category)
			.data('chosen', false)
			.appendTo($category_list);
		});

		$intro.fadeOut('fast', function() {
			$scene_a.fadeIn();
			scene_a();
		});

	});

	// Scene A: Choose from different categories
	function scene_a(){
		var all_categories = $category_list.find('div');
		all_categories.on('click', function(e){
			var chosen = $(this).data('chosen');
			var current_category = $(this);
			if(chosen) {
				current_category.data('chosen', false);
				current_category.removeClass('active');

			} else {
				current_category.data('chosen', true);
				current_category.addClass('active');
			}
			buildChosen();
			e.preventDefault();
		});

		function buildChosen() {
			chosen_categories = [];
			$.each(all_categories, function(c) {
				if($(this).data('chosen')) {
					chosen_categories.push($(this).data('category'));
				}
			});

			if(chosen_categories.length) {
				$goto_b.removeAttr('disabled');
			} else {
				$goto_b.attr('disabled', 'disabled');
			}
		}

		$goto_b.on('click', function(e) {
			$scene_a.fadeOut('fast', function() {
				$scene_b.fadeIn();
				scene_b();
			});
			e.preventDefault();
		});

	}

	// Scene B: choose one category and make a confession
	function scene_b() {
		$.each(chosen_categories, function(id, category) {
			var $category_box = $('<div>').html(category.name)
			.data('category', category);

			$('<span>')
			.addClass('percent')
			.html(helpers.percent(category.total, total_confessions) + '%')
			.appendTo($category_box);


			$category_box.appendTo($chosen_category_list);
		});

		$chosen_category_list.find('div').draggable();
		$dropspot.droppable({
			tolerance: 'touch',
			drop: function(event, ui) {
				var $drop = ui.draggable;
				final_category = $drop.data('category');
				$drop.hide();
				$dropspot.slideUp();
				$form.slideDown();
				$chosen_category_list.find('div').draggable('disable');
			}
		});

		$confession.on('keyup', function() {
			if($(this).val().length) {
				$goto_c.removeAttr('disabled');
			} else {
				$goto_c.attr('disabled', 'disabled');
			}
		});

		$goto_c.on('click', function(e) {
			confession = {
				category: final_category.id,
				text: $confession.val(),
				score: $score.val()
			};

			helpers.request('/confess', confession, function(response) {
				$scene_b.fadeOut('fast', function() {
					$scene_c.fadeIn();
					scene_c(response);
				});
			});

			e.preventDefault();

		});

	}

	// Scene C: comparte to another Confession
	function scene_c(other) {
		$mine.html(confession.text);
		$other.html(other.text);

		$better.on('click', function(e){
			confession.score = Math.max(0, confession.score - 1);
			other.score = Math.min(5, other.score + 1);
			process();
		});

		$worse.on('click', function(e){
			confession.score = Math.min(5, confession.score + 1);
			other.score = Math.max(0, other.score - 1);
			process();
		});

		function process() {
			var payload = {
				'mine': confession,
				'other': other
			};

			helpers.request('/save', payload, function(response) {
				$pad.slideUp();
				$enter.slideDown();
				$go.on('click', function() {
					$scene_c.fadeOut('fast', function() {
						$scene_d.fadeIn();
						scene_d(response);
					});
				});
			});
		}
	}

	function scene_d(data) {
		$final_my.html(data.mine.text + ' Score: ' + data.mine.score);
		$.each(data.other, function(id, other) {
			$('<div>')
			.html(other.text + ' Score: ' + other.score)
			.appendTo($final_other);
		});
	}

})(jQuery);
