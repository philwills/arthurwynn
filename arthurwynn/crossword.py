from google.appengine.ext import db

class Crossword(db.Model):
	name = db.StringProperty()
	number = db.IntegerProperty()
	type = db.StringProperty()
	creator = db.StringProperty()
	num_grid_rows = db.IntegerProperty()
	num_grid_cols = db.IntegerProperty()
	across_solutions = db.StringListProperty()
	across_clues = db.StringListProperty()
	across_x = db.ListProperty(int)
	across_y = db.ListProperty(int)
	across_nums = db.ListProperty(int)
	down_solutions = db.StringListProperty()
	down_clues = db.StringListProperty()
	down_x = db.ListProperty(int)
	down_y = db.ListProperty(int)
	down_nums = db.ListProperty(int)
	date = db.DateTimeProperty(auto_now_add=True)
	xml = db.TextProperty()

	def size(self, size):
		self.num_grid_rows = size
		self.num_grid_cols = size

	def grid_height(self):
		return self.num_grid_rows * 2 + 0.1;

	def grid_width(self):
		return self.num_grid_cols * 2;

	def grid_rows(self):
		return range(1, self.num_grid_rows + 1)

	def grid_cols(self):
		return range(1, self.num_grid_cols + 1)

	def across_words(self):
		return [Word(self.across_nums[i], self.across_clues[i], self.across_solutions[i], self.across_x[i], self.across_y[i], "across") for i in range(len(self.across_nums))]

	def down_words(self):
		down_words = [Word(self.down_nums[j], self.down_clues[j], self.down_solutions[j], self.down_x[j], self.down_y[j], "down") for j in range(len(self.down_nums))]
		down_words.sort()
		for i in range(len(self.down_nums)):
			down_words[i].number = self.down_nums[i] 
			down_words[i].clue = self.down_clues[i] 
		return down_words

	def words(self):
		words = self.across_words()
		words.extend(self.down_words())
		return words

	def intersections(self):
		across_letters = {}
		for across_word in self.across_words():
			for i in range(len(across_word.solution)):
				across_letters[str(across_word.x + i) + '-' + str(across_word.y)] = str(across_word.number) + '-across-' + str(i + 1)
		down_letters = {}
		for down_word in self.down_words():
			for i in range(len(down_word.solution)):
				down_letters[str(down_word.x) + '-' + str(down_word.y + i)] = str(down_word.number) + '-down-' + str(i + 1)
		intersections = {}
		for coordinate in across_letters.keys():
			if coordinate in down_letters:
				intersections[across_letters[coordinate]] = down_letters[coordinate]
		return intersections
	
	def build_solution(self, letters):
		in_word = False
		self.across_solutions = []
		self.across_x = []
		self.across_y = []
		for row_num in self.grid_rows():
			current_word = ""
			for col_num in self.grid_cols():
				letter = letters[col_num, row_num]
				next_letter_is_empty = col_num == self.num_grid_cols or len(letters[col_num + 1, row_num]) == 0
				if in_word:
					current_word = current_word + letter
					if next_letter_is_empty:
						in_word = False
						self.across_solutions.append(current_word)
						current_word = ""
				elif len(letter) > 0 and not next_letter_is_empty:
					in_word = True
					self.across_x.append(col_num - 1)
					self.across_y.append(row_num - 1)
					current_word = current_word + letter
		in_word = False
		self.down_solutions = []
		self.down_x = []
		self.down_y = []
		for col_num in self.grid_cols():
			current_word = ""
			for row_num in self.grid_rows():
				letter = letters[col_num, row_num]
				next_letter_is_empty = row_num == self.num_grid_rows or len(letters[col_num, row_num + 1]) == 0
				if in_word:
					current_word = current_word + letter
					if next_letter_is_empty:
						in_word = False
						self.down_solutions.append(current_word)
						current_word = ""
				elif len(letter) > 0 and not next_letter_is_empty:
					in_word = True
					self.down_x.append(col_num - 1)
					self.down_y.append(row_num - 1)
					current_word = current_word + letter
		self.calculate_numbers()

	def build_clues(self, across_clues, down_clues):
		self.across_clues = []
		for num in self.across_nums:
			self.across_clues.append(across_clues[str(num)])
		self.down_clues = []
		for num in self.down_nums:
			self.down_clues.append(down_clues[str(num)])

	def calculate_numbers(self):
		number = 1
		across_x_and_y = [self.across_x, self.across_y]
		across_coords = zip(*across_x_and_y)
		down_x_and_y = [self.down_x, self.down_y]
		down_coords = zip(*down_x_and_y)
		self.across_nums = []
		self.down_nums = []
		for row_num in self.grid_rows():
			for col_num in self.grid_cols():
				if (col_num - 1, row_num - 1) in across_coords:
					self.across_nums.append(number)
					self.across_clues.append('')
				if (col_num - 1, row_num - 1) in down_coords:
					self.down_nums.append(number)
					self.down_clues.append('')
				if (col_num - 1, row_num - 1) in across_coords or (col_num - 1, row_num - 1) in down_coords:
					number = number + 1
				
class Word:
	def dis_x(self):
		return self.x * 2

	def dis_y(self):
		return self.y * 2

	def __init__(self, num, clue, solution, x, y, direction):
		self.number = num
		self.clue = clue
		self.solution = solution
		self.x = x
		self.y = y
		self.direction = direction

	def __cmp__(self, other):
		y_comparison = cmp(self.y, other.y)
		if y_comparison is not 0:
			return y_comparison
		else:
			return cmp(self.x, other.x)
