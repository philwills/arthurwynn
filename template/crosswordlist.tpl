<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
	<head>
		<title>Arthur Wynn Appreciation Crosswords</title>
		<link rel="alternate" type="application/atom+xml" title="Arthur Wynn Appreciation Crosswords - Atom" href="http://arthur-wynn.appspot.com/atom.xml" />
		<style type="text/css">
			body {
				font-family: geneva, sans-serif;
			}
		</style>
	</head>
	<body>
		<h1>Latest Crosswords</h1>
		<ol>
		{% for crossword in crosswords %}
			<li><a href="crossword?key={{ crossword.key }}">{{ crossword.title }}</a></li>
		{% endfor %}
		</ol>
		<a href="create">Create a new crossword</a>
	</body>
</html>
