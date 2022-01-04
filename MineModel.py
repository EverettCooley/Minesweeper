import random

class MineModel():

	row_count = None
	col_count = None
	neighboring_bombs_grid = [] # holds the number of neighboring bombs to the current square, for each square
	uncovered_grid = [] # holds what squares are shown to the user
	seen_points_list = [] # prevents recursion from loop back to old squares


	def __init__(self, row_count, col_count, bomb_n):

		self.row_count = row_count
		self.col_count = col_count

		# setup grid and uncover gird
		for i in range(self.row_count):
			temp = []
			for j in range(self.col_count):
				temp.append("#")
			temp_copy = temp.copy()
			self.neighboring_bombs_grid.append(temp)
			self.uncovered_grid.append(temp_copy)

		# fills grid with bombs
		if ((self.row_count * self.col_count) > bomb_n):
			for _ in range(bomb_n):
				row = random.randint(0,col_count - 1)
				col = random.randint(0, row_count - 1)
				
				while self.bomb_error_checker(row, col):
					row = random.randint(0,col_count - 1)
					col = random.randint(0, row_count - 1)

		# adds each square with the respective bomb neighbor count
		for i in range(self.row_count):
			for j in range(self.col_count):
				self.neighboring_bombs_grid[i][j] = str(self.n_bomb_neighbors(i,j))

		
	# returns the number of bomb neighbors from a given point
	def n_bomb_neighbors(self, row, col):

		bomb_count = 0
		if self.neighboring_bombs_grid[row][col] == 'b':
			return 'b'

		for i in range(3):
			# scans the row above givn point
			temp_row = row - 1
			temp_col = col - 1 + i
			if (temp_row >= 0) and (temp_col >= 0) and (temp_col < self.col_count) and (temp_row < self.row_count):
				if self.neighboring_bombs_grid[temp_row][temp_col] == "b":
					bomb_count += 1

			# scans the row above givn point
			temp_row = row + 1
			if (temp_row >= 0) and (temp_col >= 0) and (temp_col < self.col_count) and (temp_row < self.row_count):
				if self.neighboring_bombs_grid[temp_row][temp_col] == "b":
					bomb_count += 1

		# scans to the right 
		temp_col = col + 1
		if (temp_col >= 0) and (temp_col < self.col_count):
			if self.neighboring_bombs_grid[row][temp_col] == "b":
				bomb_count += 1

		# scans to the left
		temp_col = col - 1 
		if (temp_col >= 0) and (temp_col < self.col_count):
			if self.neighboring_bombs_grid[row][temp_col] == "b":
				bomb_count += 1

		return bomb_count


	# checks if the user has won
	def has_won(self):
		for i in range(self.row_count):
			for j in range(self.col_count):
				if (self.neighboring_bombs_grid[i][j] != "b") and (self.uncovered_grid[i][j] == "#"):
					return False
		return True
	

	def get_uncovered_grid(self):
		return self.uncovered_grid


	def get_neighboring_bombs_grid(self):
		return self.neighboring_bombs_grid


	# checks if a bomb is located at a given location if not places a bomb there
	def bomb_error_checker(self, row, col):
		if self.neighboring_bombs_grid[row][col] == "b":
			return True
		self.neighboring_bombs_grid[row][col] = "b"


	# changes grid status to, shown to the player
	def uncover_square(self, row, col):
		self.uncovered_grid[row][col] = "_"


	# checks if bomb is located at a location
	def bomb_located(self, row, col):
		if self.neighboring_bombs_grid[row][col] == 'b':
			return True


	# expand the grid recursivly like the true minesweeper game
	def expand_grid(self, row, col):

		# reveal current
		self.uncover_square(row, col)

		# if greater than 0 return 
		if int(self.neighboring_bombs_grid[row][col]) > 0:
			return

		# ABOVE: check if above neighbor is within bounds. If yes, jump to it
		next_square = [str(row - 1), str(col)]
		if next_square not in self.seen_points_list:
			if (row - 1 >= 0):
				self.seen_points_list.append(next_square)
				self.expand_grid(row - 1, col)

		# BELOW
		next_square = [str(row + 1), str(col)]
		if next_square not in self.seen_points_list:
			if (row < self.row_count - 1):
				self.seen_points_list.append(next_square)
				self.expand_grid(row + 1, col)
		
		# RIGHT
		next_square = [str(row), str(col + 1)]
		if next_square not in self.seen_points_list:
			if (col < self.col_count - 1):
				self.seen_points_list.append(next_square)
				self.expand_grid(row, col + 1)

		# LEFT
		next_square = [str(row), str(col - 1)]
		if [str(row), str(col - 1)] not in self.seen_points_list:
			if (col - 1 >= 0):
				self.seen_points_list.append([str(row), str(col - 1)])
				self.expand_grid(row , col - 1)
		
		# ABOVE-LEFT
		next_square = [str(row - 1), str(col - 1)]
		if next_square not in self.seen_points_list:
			if (row - 1 >= 0) and (col - 1 >= 0):
				self.seen_points_list.append(next_square)
				self.expand_grid(row - 1, col - 1)

		# ABOVE-RIGHT
		next_square = [str(row - 1), str(col + 1)]
		if next_square not in self.seen_points_list:
			if (row - 1 >= 0) and (col < self.col_count - 1):
				self.seen_points_list.append(next_square)
				self.expand_grid(row - 1, col + 1)

		# BELOW-RIGHT
		next_square = [str(row + 1), str(col + 1)]
		if next_square not in self.seen_points_list:
			if (row < self.row_count - 1) and (col < self.col_count - 1):
				self.seen_points_list.append(next_square)
				self.expand_grid(row + 1, col + 1)
		
		# BELOW-LEFT
		next_square = [str(row + 1), str(col - 1)]
		if next_square not in self.seen_points_list:
			if (row < self.row_count - 1) and (col - 1 >= 0):
				self.seen_points_list.append(next_square)
				self.expand_grid(row + 1, col - 1)


	# handles player grid square expansion
	def expansion_handler(self, row, col):
		self.expand_grid(row, col)
		self.seen_points_list = [] # reset seen list
