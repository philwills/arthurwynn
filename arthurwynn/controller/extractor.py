from xml.etree.ElementTree import fromstring

class CrosswordDotInfoXmlExtractor():
	def parse(self, xml_string):
		self.root = fromstring(xml_string)
		self.namespace = '{http://crossword.info/xml/rectangular-puzzle}'
		self.puzzle = self.root.find('./' + self.namespace + 'rectangular-puzzle/')
		self.grid = self.puzzle.find('./' + self.namespace + 'crossword/' + self.namespace + 'grid')
		self.across_clue_dict = {}
		self.down_clue_dict = {}
		self.extract_clues()

	def title(self):
		return self.type().capitalize() + ' Crossword No. ' + str(self.identifier())

	def type(self):
		titleText = self.puzzle.find('./' + self.namespace + 'metadata/' + self.namespace + 'title').text
		if titleText[0:4] == 'gdn.':
			return titleText[4:]

	def creator(self):
		return self.puzzle.find('./' + self.namespace + 'metadata/' + self.namespace + 'creator').text
		
	def identifier(self):
		return int(self.puzzle.find('./' + self.namespace + 'metadata/' + self.namespace + 'identifier').text)
		
	def width(self):
		return int(self.grid.get('width'))
		
	def height(self):
		return int(self.grid.get('height'))

	def letters(self):
		letters = {}
		for cell in self.grid.findall('./' + self.namespace + 'cell'):
			if cell.get('solution'):
				letters[int(cell.get('x')), int(cell.get('y'))] = cell.get('solution')
			else:
				letters[int(cell.get('x')), int(cell.get('y'))] = ''
		return letters

	def across_clues(self):
		return self.across_clue_dict

	def down_clues(self):
		return self.down_clue_dict

	def extract_clues(self):
		for clues in self.puzzle.findall('./' + self.namespace + 'crossword/' + self.namespace + 'clues'):
			if (clues.find('./' + self.namespace + 'title/' + self.namespace +'b').text == 'Across'):
				for clue in clues.findall('./' + self.namespace + 'clue'):
					self.add_clue(self.across_clue_dict, clue)
			else:
				for clue in clues.findall('./' + self.namespace + 'clue'):
					self.add_clue(self.down_clue_dict, clue)

	def add_clue(self, clue_dict, clue):
		clue_numbers = clue.get('number').split(',')
		clue_dict[clue_numbers[0]] = self.get_clue_text(clue)
		if (len(clue_numbers) > 1 and clue_numbers[1] not in clue_dict and not clue_numbers[1].endswith('down')):
			clue_dict[clue_numbers[1]] = 'See ' + clue_numbers[0]

	def get_clue_text(self, clue):
		if (clue.get('format')):
			return clue.text + ' (' + clue.get('format') + ')'
		else:
			return clue.text

class GuCrosswordXmlExtractor():
	def parse(self, xml_string):
		self.root = fromstring(xml_string)

	def title(self):
		return self.root.find('./header/title').text

	def type(self):
		return self.root.attrib['type']

	def creator(self):
		return self.root.find('./header/author').text

	def identifier(self):
		return int(self.root.attrib['serial'])

	def width(self):
		return int(self.root.find('./header/grid').attrib['cols'])
		
	def height(self):
		return int(self.root.find('./header/grid').attrib['rows'])

	def letters(self):
		pass
