var jQ = jQuery.noConflict();

jQ('ready', crossword_init);
if (typeof(addSafeLoadEvent) !== 'undefined') {
	addSafeLoadEvent(crossword_init);
}
jQ('ready', load_from_cookie);

var active_word;

function crossword_init() {
	var inputs = jQ('#grid').find('input');

	inputs.bind('focus', function(e) {
		this.select();

		activate_word(jQ(this));
	});

	inputs.bind('click', function(e) {
		var current_letter = jQ(this);
		var word = current_letter.closest('div');
		var intersecting_letter = getIntersectingLetter(current_letter);
		if (intersecting_letter && active_word && word.attr('id') == active_word.attr('id')) {
			deactivate_word(current_letter);
			activate_word(intersecting_letter);
			intersecting_letter.focus();
		} 
	});

	inputs.bind('blur', function(e) {
		var current_letter = jQ(this);
		deactivate_word(current_letter);
		var intersecting_letter = getIntersectingLetter(current_letter);
		if (intersecting_letter) {
			deactivate_word(intersecting_letter);
		}
	});

	inputs.bind('keyup', function(e) {
		copyChangeToIntersectingLetter(jQ(e.target));
		focusOnNextInput(jQ(e.target));
	});

	inputs.bind('keyup', 'tab', function(e) {
		if (jQ(e.target).closest('div').next('div')) {
			jQ(e.target).closest('div').next('div').find('input:first').focus();
		}
		return false;
	});
	inputs.bind('keyup', 'Shift+tab', function(e) {
		if (jQ(e.target).closest('div').prev('div')) {
			jQ(e.target).closest('div').prev('div').find('input:first').focus();
		}
		return false;
	});
	inputs.bind('keyup', 'left', function(e) {
		move_back(e, 'across');
		return false;
	});
	inputs.bind('keyup', 'up', function(e) {
		move_back(e, 'down');
		return false;
	});
	inputs.bind('keyup', 'right', function(e) {
		move_forward(e, 'across');
		return false;
	});
	inputs.bind('keyup', 'down', function(e) {
		move_forward(e, 'down');
		return false;
	});
	inputs.bind('keyup', 'backspace', function(e) {
		focusOnPreviousInput(jQ(e.target));
	});	
	inputs.bind('keyup', 'del', function(e) {
		// Capture action to stop moving cursor
		return false;
	});	

	function move_back(e, direction) {
		var letter = jQ(e.target);
		if (letter.attr('id').indexOf(direction) !== -1) {
			focusOnPreviousInput(letter);
		} else {
			if (getIntersectingLetter(letter)) {
				focusOnPreviousInput(getIntersectingLetter(letter));
			}
		}
	}
	function move_forward(e, direction) {
		var letter = jQ(e.target);
		if (letter.attr('id').indexOf(direction) !== -1) {
			focusOnNextInput(letter);
		} else {
			if (getIntersectingLetter(letter)) {
				focusOnNextInput(getIntersectingLetter(letter));
			}
		}
	}

	jQ('label').bind('click', function(e) {
		activate_word(jQ('#' + jQ(e.target).attr('for')));
		e.stop();
	});

	jQ('#check').bind('click', function(e) {
		check(active_word.find('input'));
	});

	jQ('#check-all').bind('click', function(e) {
		check(inputs);
	});

	jQ('#cheat').bind('click', function(e) {
		active_word.find('input').each(function(index, input) {
			var square = jQ(input);
			square.val(solutions[square.attr('id')].toLowerCase());
			copyChangeToIntersectingLetter(square);
		});
	});

	jQ('#clear').bind('click', function(e) {
		clear(active_word.find('input'));
	});

	jQ('#save').bind('click', function(e) {
		var form_values = jQ(this).closest('form').serialize();
		jQ.cookie(crossword_identifier, form_values, { expires: 365 });
	});

	jQ('#revert-to-saved').bind('click', function(e) {
		load_from_cookie();
	});
}

function load_from_cookie() {
	var saved_state = jQ.cookie(crossword_identifier);
	if (saved_state) {
		jQ(saved_state.split('&')).each(function(index, pair) {
			var name_value = pair.split('=');
			jQ('#' + name_value[0]).val(name_value[1]);
		});
	}
}

jQ('ready', bind_activate);
function bind_activate() {
	jQ('#anagrams').bind('click', function(e) {
		var existing_letters = "";
		active_word.find('input').each(function(index, input) {
			var letter = jQ(input);
			if (letter.val()) {
				existing_letters += letter.val();
			} else {
				existing_letters += '_';
			}
		});
		var width = existing_letters.length * 35;
		var height = width + 35;
		window.open('/anagram?existing_letters=' + existing_letters, 'anagrams', 'toolbar=false,menubar=false,status=false,height=' + height + ',width=' + width);
	});
}

function focusOnNextInput(element) {
	var nextClue = element.parent().next();
	if(nextClue) {
		nextClue.find('input').focus();
	}
}

function focusOnPreviousInput(element) {
	var previousClue = element.parent().prev();
	if(previousClue) {
		previousClue.find('input').focus();
	}
}

function getIntersectingLetter(letter) {
	if(intersections[letter.attr('id')]) {
		return jQ('#' + intersections[letter.attr('id')]);
	}
	return null;
}
	

function copyChangeToIntersectingLetter(letter) {
	var intersect = getIntersectingLetter(letter);
	if (intersect) {
		intersect.val(letter.val());
	}
}

function activate_word(letter) {
	if (active_word) {
		deactivate_word(active_word.find('input')[0]);
	}
	var word = letter.closest('div');
	word.addClass('active');
	jQ('#' + word.attr('id') + '-clue').addClass('active');
	active_word = word;
}

function deactivate_word(letter) {
	var word = jQ(letter).closest('div');
	word.removeClass('active');
	jQ('#' + word.attr('id') + '-clue').removeClass('active');
}

function insert_from_anagram(letter_array) {
	active_word.find('input').each(function(index, letter) {
		jQ(letter).val(letter_array[index]);
		copyChangeToIntersectingLetter(jQ(letter));
	});
}

function clear(input_array) {
	input_array.each(function(index, input) {
		var square = jQ(input);
		square.val('');
		copyChangeToIntersectingLetter(square);
	});
}

function check(input_array) {
	input_array.each(function(index, input) {
		var square = jQ(input);
		if (square.val().toLowerCase() != solutions[square.attr('id')].toLowerCase()) {
			square.val('');
			copyChangeToIntersectingLetter(square);
		}
	});
}
