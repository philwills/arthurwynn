from google.appengine.ext import webapp

register = webapp.template.create_template_register()

@register.filter
def alphabetise(number):
	if number == 1: return 'A'
	if number == 2: return 'B'
	if number == 3: return 'C'
	if number == 4: return 'D'
	if number == 5: return 'E'
	if number == 6: return 'F'
	if number == 7: return 'G'
	if number == 8: return 'H'
	if number == 9: return 'I'
	if number == 10: return 'J'
	if number == 11: return 'K'
	if number == 12: return 'L'
	if number == 13: return 'M'
	if number == 14: return 'N'
	if number == 15: return 'O'
	if number == 16: return 'P'
	if number == 17: return 'Q'
	if number == 18: return 'R'
	if number == 19: return 'S'
	if number == 20: return 'T'
	if number == 21: return 'U'
	if number == 22: return 'V'
	if number == 23: return 'W'
	if number == 24: return 'X'
	if number == 25: return 'Y'
	if number == 26: return 'Z'
