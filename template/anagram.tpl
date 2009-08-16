<html>
<head>
<title>Anagram</title>
<script type="text/javascript" src="/microapp/assets/js/moo.js"></script>
<script type="text/javascript">
window.addEvent('domready', activate_shuffle);
window.addEvent('domready', activate_insert);
window.addEvent('domready', setup_letters);

function activate_shuffle() {
	$('shuffle').addEvent('click', shuffle_letters);
}

function activate_insert() {
	$('insert').addEvent('click', insert_to_opener);
}

function setup_letters() {
	$('anagrams').getElements('input').addEvent('keyup', arrange_letters);
}

function shuffle_letters() {
	var letters = [];
	get_anagram_inputs().each(function(input) {
		if (input.type === 'text' && input.className !== 'fixed') {
			letters[letters.length] = input.value;
		}
	});
	shuffle(letters);
	get_anagram_inputs().each(function(input) {
		if (input.className !== 'fixed') {
			input.value = letters.pop();
		}
	});
	arrange_letters();
	return false;
}

function insert_to_opener() {
	var letters = [];
	get_anagram_inputs().each(function(input) {
		letters[letters.length] = input.value;
	});
	window.opener.insert_from_anagram(letters);
	window.close();
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
	get_anagram_inputs().each(function(input) {
		if (input.className !== 'fixed' && input.value !== '') {
			unfixed_letters.push(input.value);
		}
	});
	var radius = 8 * get_anagram_inputs().length;
	unfixed_letters.each(function(letter, index) {
		var positioned_letter = new Element('span', {
			'html': letter,
		});
		positioned_letter.setStyles({
			'position': 'absolute',
			'top': radius * Math.sin(2 * Math.PI * index / unfixed_letters.length - Math.PI / 2) + radius + 15,
			'left': radius * Math.cos(2 * Math.PI * index / unfixed_letters.length - Math.PI / 2) + radius + 15,
		});
		positioned_letter.inject($('letters'));
	});
}

function get_anagram_inputs() {
	return $('anagrams').getElements('input');
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
		border: 1px solid;
		font-variant: small-caps;
		display: block;
		float: left;
	}
	#anagrams input.fixed {
		border: 2px solid;
	}
	#buttons {
		display: block;
		clear: left;
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
<div id="buttons">
	<button id="shuffle">Shuffle</button>
	<button id="insert">Insert</button>
</div>
</form>
</body>
</html>
