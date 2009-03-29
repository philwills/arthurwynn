<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom'>
<id>http://arthur-wynn.appspot.com/</id>
<title>Latest Crosswords</title>
<updated>{{ latestdate|date:"r" }}</updated>
{% for crossword in crosswords %}
<entry>
	<id>http://arthur-wynn.appspot.com/crossword?key={{ crossword.key }}</id>
	<title>{{ crossword.name|escape }}</title>
	<updated>{{ crossword.date|date:"r" }}</updated>
	<link rel="alternate" href="http://arthur-wynn.appspot.com/crossword?key={{ crossword.key }}"/>
</entry>
{% endfor %}
</feed>
