<html>
	<head>
		<title>Crossword {{crossword.name}}</title>
		<link rel="stylesheet" type="text/css" href="/css/crossword.css"/>
		<style type="text/css">
			div#grid {
				width: {{ crossword.grid_width }}em;
			}
		</style>
		<script type="text/javascript" src="/js/moo.js"></script>
		<script type="text/javascript">
			window.addEvent('domready', crossword_init);

			function crossword_init() {
				var inputs = $$('input');
				
				inputs.addEvent('keyup', function(e) {
					if (e.key == 'down') {
						column = this.className;
						this.getParent('li.row').getNext().getElement('input.' + column).focus();
						e.stop();
						return;
					}
					if (e.key == 'up') {
						column = this.className;
						this.getParent('li.row').getPrevious().getElement('input.' + column).focus();
						e.stop();
						return;
					}
					if (e.key == 'left') {
						focusOnPreviousInput(this);
						e.stop();
						return;
					}	
					if (e.key == 'right') {
						focusOnNextInput(this);
						e.stop();
						return;
					}	
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
		</script>
	</head>
	<body>
	<form method="POST">
		<div id="grid">
			<ol>
			{% for row in crossword.grid_rows %}
				<li class="row"><ol>
				{% for col in crossword.grid_cols %}
					<li><input name="{{ col }}-{{ row }}" type="text" maxlength="1" class="{{ col }}" autocomplete="off" /></li>
				{% endfor %}
				</ol></li>
			{% endfor %}
			</ol>
		</div>

		<input type="hidden" name="key" value="{{ crossword.key }}" />
		<input type="submit" name="submit" class="submit" value="Add Clues" />
	</form>
</html>
