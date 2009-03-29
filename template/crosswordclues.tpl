<html>
	<head>
		<title>Crossword {{crossword.name}}</title>
		<link rel="stylesheet" type="text/css" href="/css/crossword.css"/>
		<style type="text/css">
		#grid {
			width: {{crossword.grid_width}}em; 
			height: {{crossword.grid_height}}em; 
		}
		</style>
	</head>
	<body>
	<form method="POST">
	<div id="grid">
		{% for word in crossword.words %}
		<div id="{{ word.number }}-{{ word.direction }}" style="left: {{ word.dis_x }}em; top: {{ word.dis_y }}em;" class="{{ word.direction }}">
			<fieldset>
				<legend>{{ word.number }} {{ word.direction }}</legend>
				<ol>
			{% for char in word.solution|make_list %}
					<li>{% if forloop.first %}<span>{{ word.number }}</span>{% endif %}<input type="text" value="{{char}}" size="1" maxlength="1" /></li>
			{% endfor %}
				</ol>
		</div>
		{% endfor %}
	</div>
	<div id="clues">
		 ACROSS
        <ol>
        {% for across_num in crossword.across_nums %}
            <li>{{ across_num }}<input name="{{ across_num }}-across" type="text"/></li>
        {% endfor %}
        </ol>
        DOWN
        <ol>
        {% for down_num in crossword.down_nums %}
            <li>{{ down_num }}<input name="{{ down_num }}-down" type="text"/></li>
        {% endfor %}
        </ol>
	</div>
	<input type="submit" value="Finish" />
	</form>
</html>
