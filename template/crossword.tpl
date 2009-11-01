<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"> 
<html>
	<head>
		<title>Crossword {{crossword.name}}</title>
		<link rel="stylesheet" type="text/css" href="/css/crossword.css"/>
		<link rel="stylesheet" type="text/css" href="/css/print.css" media="print" />
		<script type="text/javascript" src="/js/jquery.js"></script>
		<script type="text/javascript" src="/js/jquery.hotkeys-0.7.9.js"></script>
		<script type="text/javascript" src="/js/jquery.cookie.js"></script>
		<script type="text/javascript" src="/js/crossword.js"></script>
	</head>
	<body>
		<script type="text/javascript">
		var crossword_identifier = 'crossword-{{ crossword.key }}';
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
