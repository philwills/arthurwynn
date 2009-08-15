<html>
<head>
<title>Anagram</title>
<script type="text/javascript" src="/microapp/assets/js/moo.js"></script>
<script type="text/javascript">
window.addEvent('domready', activate_shuffle);
window.addEvent('domready', setup_letters);

function activate_shuffle() {
	$('shuffle').addEvent('click', shuffle_letters);
}

function setup_letters() {
	$('anagrams').getElements('input').addEvent('keyup', arrange_letters);
}

function shuffle_letters() {
	var letters = [];
	$('anagrams').getElements('input').each(function(input) {
		if (input.type === 'text' && input.className !== 'fixed') {
			letters[letters.length] = input.value;
		}
	});
	shuffle(letters);
	$('anagrams').getElements('input').each(function(input) {
		if (input.className !== 'fixed') {
			input.value = letters.pop();
		}
	});
	arrange_letters();
	return false;
}

function shuffle ( arr ) {
	var i = arr.length;
	if ( i == 0 ) return false;
	while ( --i ) {
		var j = Math.floor( Math.random() * ( i + 1 ) );
		var tempi = arr[i];
		var tempj = arr[j];
		arr[i] = tempj;
		arr[j] = tempi;
	}
}

function arrange_letters() {
	$('letters').empty();
	var unfixed_letters = [];
	$('anagrams').getElements('input').each(function(input) {
		if (input.className !== 'fixed' && input.value !== '') {
			unfixed_letters.push(input.value);
		}
	});
	var radius = 8 * $('anagrams').getElements('input').length;
	unfixed_letters.each(function(letter, index) {
		var positioned_letter = new Element('span', {
			'html': letter,
		});
		positioned_letter.setStyles({
			'position': 'absolute',
			'top': radius * Math.sin(2 * Math.PI * index / unfixed_letters.length - Math.PI / 2) + radius + 10,
			'left': radius * Math.cos(2 * Math.PI * index / unfixed_letters.length - Math.PI / 2) + radius + 10,
		});
		positioned_letter.inject($('letters'));
	});
}
</script>
<style type="text/css">
	#letters {
		position: relative;
		font-variant: small-caps;
	}
	#anagrams {
		position: absolute;
		bottom: 1em;
	}
	#anagrams input {
		font-variant: small-caps;
	}
</style>
</head>
<body>
<div id="letters"></div>
<form id="anagrams">
{% for letter in letters %}
	{% ifequal letter '_' %}
		<input type="text" maxlength="1" size="1">
	{% else %}
		<input type="text" maxlength="1" size="1" value="{{ letter }}" class="fixed">
	{% endifequal %}
{% endfor %}
<button id="shuffle">Shuffle</button>
</form>
</body>
</html>
