import random

# self.grid = [["#","#","#","#"], # "#" = unclicked
#         	   ["#","#","#","#"], # "_" = clicked
#         	   ["#","#","#","b"], # "b" = bomb
#         	   ["#","#","#","#"]]

class MineModel():
	def __init__(self, row_n, col_n, bomb_n):

		self.row_n = row_n
		self.col_n = col_n
		self.bomb_n = int(bomb_n)
		self.grid = [] # main grid that holds the number of bomb neighbors on each square
		self.uncovered_grid = [] # holds what squares are shown to the user
		self.seen_points_list = [] # prevents recursion from loop back to old squares

		# setup grid
		for i in range(self.row_n):
			temp_l = []
			for j in range(self.col_n):
				temp_l.append("#")
			self.grid.append(temp_l)
		
		# setup uncovered_grid that holds which squares should have their bomb numbers shown
		for i in range(self.row_n):
			temp_l = []
			for j in range(self.col_n):
				temp_l.append("#")
			self.uncovered_grid.append(temp_l)

		# fills grid with bombs
		if ((self.row_n * self.col_n) > self.bomb_n):
			self.fill_grid_with_bombs(self.row_n,self.col_n, self.bomb_n)

		# adds each square with the respective bomb neighbor count
		self.add_bomb_neighbor_count()

	# checks if the user has won
	def has_won(self):
		for i in range(self.row_n):
			for j in range(self.col_n):
				if (self.grid[i][j] != "b") and (self.uncovered_grid[i][j] == "#"):
					return False
		return True

	def get_uncovered_grid(self):
		return self.uncovered_grid

	def get_grid(self):
		return self.grid

	# checks if a bomb is located at a given location if not places a bomb there
	def bomb_error_checker(self, x, y):
		if self.grid[x][y] == "b":
			return True
		self.grid[x][y] = "b"

	def fill_grid_with_bombs(self, row_count, col_count, number_of_bombs):
		for _ in range(number_of_bombs):

			x = random.randint(0,col_count - 1)
			y = random.randint(0, row_count - 1)
			
			while self.bomb_error_checker(x, y):
				x = random.randint(0,col_count - 1)
				y = random.randint(0, row_count - 1)

	def uncover_square(self, row_i, col_i):
		self.uncovered_grid[row_i][col_i] = "_"

	def print_grid(self):
		for i in range(self.row_n):
			print(self.grid[i])

	def print_unc_grid(self):
		for i in range(self.row_n):
			print(self.uncovered_grid[i])

	# checks if bomb is located at a location
	def bomb_located(self, row_i, col_i):
		if self.grid[row_i][col_i] == 'b':
			return True

	# returns the number of bomb neighbors from a given point
	def n_bomb_neighbors(self, row, col):

		n_bombs = 0
		if self.grid[row][col] == 'b':
			return 'b'

		for i in range(3):
			# scans the row above givn point
			temp_row = row - 1
			temp_col = col - 1 + i
			if (temp_row >= 0) and (temp_col >= 0) and (temp_col < self.col_n) and (temp_row < self.row_n):
				if self.grid[temp_row][temp_col] == "b":
					n_bombs += 1

			# scans the row above givn point
			temp_row = row + 1
			if (temp_row >= 0) and (temp_col >= 0) and (temp_col < self.col_n) and (temp_row < self.row_n):
				if self.grid[temp_row][temp_col] == "b":
					n_bombs += 1

		# scans to the right 
		temp_col = col + 1
		if (temp_col >= 0) and (temp_col < self.col_n):
			if self.grid[row][temp_col] == "b":
				n_bombs += 1

		# scans to the left
		temp_col = col - 1 
		if (temp_col >= 0) and (temp_col < self.col_n):
			if self.grid[row][temp_col] == "b":
				n_bombs += 1

		return n_bombs


	# adds number of bomb neighbors on each square in main grid
	def add_bomb_neighbor_count(self): 
		for i in range(self.row_n):
			for j in range(self.col_n):
				self.grid[i][j] = str(self.n_bomb_neighbors(i,j))

	# expand the grid recursivly like the true minesweeper game
	def expand_grid(self, row_i, col_i):

		# reveal current
		self.uncover_square(row_i, col_i)

		# if greater than 0 return 
		if int(self.grid[row_i][col_i]) > 0:
			return

		# ABOVE: check if above neighbor is within bounds and jump to it
		if (row_i - 1 >= 0):
			temp = [str(row_i - 1), str(col_i)]
			if temp not in self.seen_points_list:
				self.seen_points_list.append(temp)
				self.expand_grid(row_i - 1, col_i)
		
		# ABOVE-LEFT
		if (row_i - 1 >= 0) and (col_i - 1 >= 0):
			temp = [str(row_i - 1), str(col_i - 1)]
			if temp not in self.seen_points_list:
				self.seen_points_list.append(temp)
				self.expand_grid(row_i - 1, col_i - 1)

		# BELOW-RIGH
		if (row_i < self.row_n - 1) and (col_i < self.col_n - 1):
			temp = [str(row_i + 1), str(col_i + 1)]
			if temp not in self.seen_points_list:
				self.seen_points_list.append(temp)
				self.expand_grid(row_i + 1, col_i + 1)
		
		# BELOW-LEFT
		if (row_i < self.row_n - 1) and (col_i - 1 >= 0):
			temp = [str(row_i + 1), str(col_i - 1)]
			if temp not in self.seen_points_list:
				self.seen_points_list.append(temp)
				self.expand_grid(row_i + 1, col_i - 1)

		# ABOVE-RIGHT
		if (row_i - 1 >= 0) and (col_i < self.col_n - 1):
			temp = [str(row_i - 1), str(col_i + 1)]
			if temp not in self.seen_points_list:
				self.seen_points_list.append(temp)
				self.expand_grid(row_i - 1, col_i + 1)

		# BELOW
		if (row_i < self.row_n - 1):
			temp = [str(row_i + 1), str(col_i)]
			if temp not in self.seen_points_list:
				self.seen_points_list.append(temp)
				self.expand_grid(row_i + 1, col_i)
		
		# RIGHT
		if (col_i < self.col_n - 1):
			temp = [str(row_i), str(col_i + 1)]
			if temp not in self.seen_points_list:
				self.seen_points_list.append(temp)
				self.expand_grid(row_i, col_i + 1)

		# LEFT
		if (col_i - 1 >= 0):
			temp = [str(row_i), str(col_i - 1)]
			if temp not in self.seen_points_list:
				self.seen_points_list.append(temp)
				self.expand_grid(row_i , col_i - 1)

	# handles expansion
	def expansion_handler(self, row_i, col_i):
		self.seen_points_list = []
		self.expand_grid(row_i, col_i)
