<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"> 
<html>
	<head>
		<title>Crossword {{crossword.name}}</title>
		<link rel="stylesheet" type="text/css" href="/microapp/assets/css/crossword.css"/>
		<link rel="stylesheet" type="text/css" href="/microapp/assets/css/print.css" media="print" />
	</head>
	<body>
	<h1>{{ crossword.title }}</h1>
	<p>{{ crossword.date|date:"l j F Y" }}</p>
		<h4>Blanks</h4>
		<ul>
		{% for row in crossword.blanks.items %}
			<li>
			Line {{ row.0 }}: 
			{% for blank in row.1 %}
				{{ blank|alphabetise }}
			{% endfor %}
			</li>
		{% endfor %}
		</ul>
		<h4>Across</h4>
		<ul>
		{% for word in crossword.across_words %}
			<li>{{ word.number }} ({{ word.human_y }}{{ word.human_x|alphabetise }}) {{ word.clue }} </li>
		{% endfor %}
		</ul>
		<h4>Down</h4>
		<ul>
		{% for word in crossword.down_words %}
			<li>{{ word.number }} ({{ word.human_y }}{{ word.human_x|alphabetise }}) {{ word.clue }} </li>
		{% endfor %}
		</ul>
	</body>
</html>
