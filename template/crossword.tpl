<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"> 
<html>
	<head>
		<title>Crossword {{crossword.name}}</title>
		<link rel="stylesheet" type="text/css" href="/microapp/assets/css/crossword.css"/>
		<link rel="stylesheet" type="text/css" href="/microapp/assets/css/print.css" media="print" />
		<script type="text/javascript" src="/microapp/assets/js/moo.js"></script>
		<script type="text/javascript" src="/microapp/assets/js/jquery.js"></script>
	</head>
	<body>
		<script type="text/javascript">
		var jQ = jQuery.noConflict();

		window.addEvent('domready', crossword_init);
		if (typeof(addSafeLoadEvent) !== 'undefined') {
			addSafeLoadEvent(crossword_init);
		}
		window.addEvent('domready', load_from_cookie);

		var active_word;

		function crossword_init() {
			var inputs = $('grid').getElements('input');

			inputs.addEvent('focus', function(e) {
				this.select();

				activate_word(this);
			});

			inputs.addEvent('click', function(e) {
				var word = this.getParent('div');
				var intersecting_letter = getIntersectingLetter(this);
				if (intersecting_letter && active_word && word.id == active_word.id) {
					deactivate_word(this);
					activate_word(intersecting_letter);
					intersecting_letter.focus();
				} 
			});

			inputs.addEvent('blur', function(e) {
				deactivate_word(this);
				var intersecting_letter = getIntersectingLetter(this);
				if (intersecting_letter) {
					deactivate_word(intersecting_letter);
				}
			});

			inputs.addEvent('keyup', function(e) {
				if (e.key != 'tab' && e.key != 'left' && e.key != 'up' && e.key != 'down' && e.key != 'right' && e.key != 'backspace') { 
					copyChangeToIntersectingLetter(this);
					if (!e.shift) {
						focusOnNextInput(this);
					}
				}
			});

			inputs.addEvent('keypress', function(e) {
				if (e.key == 'tab') {
					if (e.shift) {
						if (this.getParent('div').getPrevious('div')) {
							this.getParent('div').getPrevious('div').getElement('input').focus();
						}
					} else {
						if (this.getParent('div').getNext('div')) {
							this.getParent('div').getNext('div').getElement('input').focus();
						}
					}
					e.stop();
					return;
				}

				var id = this.id;
				var intersect = getIntersectingLetter(this);
				if ((e.key == 'left' && id.indexOf('across') != -1) || (e.key == 'up' && id.indexOf('down') != -1)) {
					focusOnPreviousInput(this);
					return;
				} else if (e.key == 'left' || e.key == 'up') {
					if (intersect) {
						focusOnPreviousInput(intersect);
					}
					return;
				}

				if ((e.key == 'right' && id.indexOf('across') != -1) || (e.key == 'down' && id.indexOf('down') != -1)) {
					focusOnNextInput(this);
					return;
				} else if (e.key == 'right' || e.key == 'down') {
					if (intersect) {
						focusOnNextInput(intersect);
					}
					return;
				}

				if (e.key == 'backspace') { 
					focusOnPreviousInput(this);
					return;
				}
			});

			$$('label').addEvent('click', function(e) {
				activate_word($(this.get('for')));
				e.stop();
			});

			$('check').addEvent('click', function(e) {
				active_word.getElements('input').each(function(square) {
					if (square.value.toLowerCase() != solutions[square.id].toLowerCase()) {
						square.value = '';
						copyChangeToIntersectingLetter(square);
					}
				});
			});

			$('check-all').addEvent('click', function(e) {
				inputs.each(function(square) {
					if (square.value.toLowerCase() != solutions[square.id].toLowerCase()) {
						square.value = '';
						copyChangeToIntersectingLetter(square);
					}
				});
			});

			$('cheat').addEvent('click', function(e) {
				active_word.getElements('input').each(function(square) {
					square.value = solutions[square.id].toLowerCase();
					copyChangeToIntersectingLetter(square);
				});
			});

			$('clear').addEvent('click', function(e) {
				active_word.getElements('input').each(function(square) {
					square.value = '';
					copyChangeToIntersectingLetter(square);
				});
			});

			$('save').addEvent('click', function(e) {
				var form_values = this.getParent('form').toQueryString();
				Cookie.write('crossword-{{ crossword.key }}', form_values, {duration: 365});
			});

			$('revert-to-saved').addEvent('click', function(e) {
				load_from_cookie();
			});
		}

		function load_from_cookie() {
			var saved_state = Cookie.read('crossword-{{ crossword.key }}');
			if (saved_state) {
				saved_state.split('&').each(function(pair) {
					var name_value = pair.split('=');
					$(name_value[0]).value = name_value[1];
				});
			}
		}

		window.addEvent('domready', bind_activate);
		function bind_activate() {
			$('anagrams').addEvent('click', function(e) {
				var existing_letters = "";
				active_word.getElements('input').each(function(input) {
					if (input.value) {
						existing_letters += input.value;
					} else {
						existing_letters += '_';
					}
				});
				var width = existing_letters.length * 35;
				var height = width + 35;
				window.open('http://localhost:8080/microapp/resources/anagram?existing_letters=' + existing_letters, 'anagrams', 'toolbar=false,menubar=false,status=false,height=' + height + ',width=' + width);
			});
		}

		function focusOnNextInput(element) {
			var nextClue = element.getParent().getNext();
			if(nextClue) {
				nextClue.getElement('input').focus();
			}
		}

		function focusOnPreviousInput(element) {
			var previousClue = element.getParent().getPrevious();
			if(previousClue) {
				previousClue.getElement('input').focus();
			}
		}

		function getIntersectingLetter(letter) {
			if(intersections[letter.id]) {
				return $(intersections[letter.id]);
			}
			return null;
		}
			

		function copyChangeToIntersectingLetter(letter) {
			var intersect = getIntersectingLetter(letter);
			if (intersect) {
				intersect.value = letter.value;
			}
		}

		function activate_word(letter) {
			if (active_word) {
				deactivate_word(active_word.getElements('input')[0]);
			}
			var word = letter.getParent('div');
			word.addClass('active');
			$(word.id + '-clue').addClass('active');
			active_word = word;
		}

		function deactivate_word(letter) {
			var word = letter.getParent('div');
			word.removeClass('active');
			$(word.id + '-clue').removeClass('active');
		}

		function insert_from_anagram(letter_array) {
			active_word.getElements('input').each(function(letter, index) {
				letter.value = letter_array[index];
				copyChangeToIntersectingLetter(letter);
			});
		}

		var intersections = new Array();
		{% for intersection in crossword.intersections.items %}
			intersections["{{intersection.0}}"] = "{{intersection.1}}";
			intersections["{{intersection.1}}"] = "{{intersection.0}}";
		{% endfor %}
		var solutions = new Array();
		{% for word in crossword.words %}
			{% for char in word.solution|make_list %}
				solutions["{{ word.number }}-{{ word.direction}}-{{ forloop.counter }}"] = "{{char}}";
			{% endfor %}
		{% endfor %}
		</script>
	<h1>{{ crossword.title }}</h1>
	<p>{{ crossword.date|date:"l j F Y" }}</p>
	<form id="crossword" method="POST">
		<div id="grid" style="width: {{crossword.grid_width}}em; height: {{crossword.grid_height}}em;">
		<img src="css/print-background.gif" alt="" id="print-background">
			{% for word in crossword.words %}
			<div id="{{ word.number }}-{{ word.direction }}" style="left: {{ word.dis_x }}em; top: {{ word.dis_y }}em;" class="{{ word.direction }}">
				<fieldset>
					<legend>{{ word.number }} {{ word.direction }}</legend>
					<ol>
				{% for char in word.solution|make_list %}
						<li>{% if forloop.first %}<span>{{ word.number }}</span>{% endif %}
							<input id="{{ word.number }}-{{ word.direction}}-{{ forloop.counter }}" name="{{ word.number }}-{{ word.direction}}-{{ forloop.counter }}" maxlength="1">
						</li>
				{% endfor %}
					</ol>
			</div>
			{% endfor %}
		</div>
	<div id="clues">
		<div>
			<h4>Across</h4>
			<ol>
			{% for word in crossword.across_words %}
				<li><label id="{{word.number}}-{{word.direction}}-clue" for="{{ word.number }}-{{ word.direction }}-1">{{ word.number }}.  {{ word.clue }}</label></li>
			{% endfor %}
			</ol>
        </div>
        <div>
			<h4>Down</h4>
			<ol>
			{% for word in crossword.down_words %}
				<li><label id="{{word.number}}-{{word.direction}}-clue" for="{{ word.number }}-{{ word.direction }}-1">{{ word.number }}.  {{ word.clue }}</label></li>
			{% endfor %}
			</ol>
        </div>
    </div>
	<div id="buttons" >
		<input id="check" type="button" value="Check" />
		<input id="cheat" type="button" value="Cheat" />
		<input id="clear" type="button" value="Clear" />
		<input id="check-all" type="button" value="Check All" />
		<input id="save" type="button" value="Save" />
		<input id="revert-to-saved" type="button" value="Revert to Saved" />
		<input id="anagrams" type="button" value="Anagrams" />
	</div>
	</form>
	</body>
</html>
