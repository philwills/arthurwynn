<html>
<head>
<title>Anagram</title>
<script type="text/javascript" src="/microapp/assets/js/moo.js"></script>
<script type="text/javascript">
window.addEvent('domready', activate_shuffle);

function activate_shuffle() {
	$('shuffle').addEvent('click', shuffle_letters);
}

function shuffle_letters() {
	var letters = [];
	$('anagrams').getElements('input').each(function(input) {
		if (input.type === 'text') {
			letters[letters.length] = input.value;
		}
	});
	shuffle(letters);
	$('anagrams').getElements('input').each(function(input) {
		if (input.type === 'text') {
			input.value = letters.pop();
		}
	});
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

function anagram(anagram_array) {

}
</script>
</head>
<body>
<form id="anagrams">
<input type="text" maxlength="1" size="1">
<input type="text" maxlength="1" size="1">
<input type="text" maxlength="1" size="1">
<input type="text" maxlength="1" size="1">
<input type="text" maxlength="1" size="1">
<input type="text" maxlength="1" size="1">
<input type="text" maxlength="1" size="1">
<input type="button" id="shuffle" value="Shuffle">
</form>
</body>
</html>
