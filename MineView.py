from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QFrame, QToolButton, QAction, QApplication, QMainWindow, QTextEdit, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, QTimer,QDateTime
from MineModel import *
import sys
import math

class MainWindow(QMainWindow):
	
	def __init__(self, size, bomb_n):
		super(MainWindow, self).__init__()
		
		self.row_n = int(size)
		self.col_n = int(size)
		self.bombs = int(bomb_n)
		self.new_game()

	# creates a new game state
	def new_game(self):

		self.bomb_count = self.bombs
		self.move_counter = 0
		self.flag_selector = False

		# main layout and widget
		self.layout = QVBoxLayout()
		self.centerWidget = QWidget()
		self.centerWidget.setLayout(self.layout)
		self.setCentralWidget(self.centerWidget)

		# bombs and move counter layout
		self.b_m_layout = QVBoxLayout()
		self.bombs_remaning_label = QLabel(f"Bombs: {self.bomb_count}")
		self.bombs_remaning_label.setStyleSheet("QLabel{font-size: 20pt;}")
		self.move_counter_label = QLabel("Moves: 0")
		self.move_counter_label.setStyleSheet("QLabel{font-size: 20pt;}")
		self.b_m_layout.addWidget(self.bombs_remaning_label)
		self.b_m_layout.addWidget(self.move_counter_label)

		# right buttons layout
		self.button_layout = QVBoxLayout()
		self.new_game_btn = QPushButton("New game")
		self.flag_btn = QPushButton("Add flag")
		self.button_layout.addWidget(self.flag_btn)
		self.button_layout.addWidget(self.new_game_btn)

		# Menu bar layout
		self.upperlayout = QHBoxLayout()
		
		# connect buttons
		self.new_game_btn.released.connect(self.new_game)
		self.flag_btn.released.connect(self.flag_handler)

		# timer 
		self.timer_label = QLabel()
		self.timer_label.setStyleSheet("QLabel{font-size: 30pt;}")
		self.count = 0
		self.flag = True
		self.timer = QTimer()
		self.timer.timeout.connect(self.showTime)
		self.timer.start(100)
		self.timer_label.setAlignment(Qt.AlignCenter)

		# add sub layouts to upperlayout
		self.upperlayout.addLayout(self.b_m_layout)
		self.upperlayout.addWidget(self.timer_label)
		self.upperlayout.addLayout(self.button_layout)
		
	
		# grid layout
		self.grid = QGridLayout()
		self.grid.setHorizontalSpacing(0)
		self.grid.setVerticalSpacing(0)
		self.grid.setContentsMargins(0,0,0,0)
		self.grid.setSpacing(0)
		
		self.style = ("QPushButton {background-color: rgb(110, 110, 110);"
                                "border-width: 1;"
                                "border-radius: 0;"
                                "height: 40;"
                                "width: 40;"
                                "border-style: solid;"
                                "border-color: rgb(10, 10, 10)}")
					
		self.style_pressed = ("QPushButton {background-color: rgb(220, 220, 220);"
                                "border-width: 1;"
                                "border-radius: 0;"
                                "height: 40;"
                                "width: 40;"
                                "border-style: solid;"
                                "border-color: rgb(10, 10, 10)}")
		
		self.style_bomb = ("QPushButton {background-color: rgb(220, 0, 0);"
                                "border-width: 1;"
                                "border-radius: 0;"
                                "height: 40;"
                                "width: 40;"
                                "border-style: solid;"
                                "border-color: rgb(10, 10, 10)}")
		

		# make a new model and get its main variables
		self.current_model = MineModel(self.row_n, self.col_n, self.bombs)
		self.cur_model_grid = MineModel.get_neighboring_bombs_grid(self.current_model)
		self.cur_model_uncovered_grid = MineModel.get_uncovered_grid(self.current_model)
		
		# fills the grid with buttons and connects them up to be pressed
		count = 1
		for i in range(self.row_n):
			for j in range(self.col_n):
				b_name = "b" + str(count)
				b_name = QPushButton()
				b_name.setStyleSheet(self.style)
				b_name.setProperty("myRow",i)
				b_name.setProperty("myCol",j)
				b_name.released.connect(self.button_released)
				self.grid.addWidget(b_name, i, j)
				count += 1

		# add grid to layout
		self.layout.addLayout(self.upperlayout)
		self.layout.addLayout(self.grid)

	# displays the timer
	def showTime(self):
		if self.flag:
				self.count += 1
		text = str(self.count / 10)
		self.timer_label.setText(text)

	# handler for placing flags on the squares
	def flag_handler(self):
		if self.flag_selector == True:
			self.flag_selector = False
			self.flag_btn.setText("Add Flag")
		else:
			self.flag_selector = True
			self.flag_btn.setText("Flagging")

	# checks if the player has died by choosing a square with a bomb in it
	# if so lock the screen and stop timer
	def died(self):
		total_squares = self.row_n * self.col_n
		for i in range(total_squares):
			target_btn = self.grid.itemAt(i).widget()
			self.flag = False
			target_btn.setEnabled(False)

	# checks if the player has won,if so lock the screen, stop timer and display a you won message
	def has_won(self):
		msg = QMessageBox()
		msg.setText("You won!")
		total_squares = self.row_n * self.col_n
		for i in range(total_squares):
			target_btn = self.grid.itemAt(i).widget()
			self.flag = False
			target_btn.setEnabled(False)
		x = msg.exec_() 

	# main button press handler
	def button_released(self):

		# sender info
		clicked=self.sender()
		row_i=clicked.property("myRow")
		col_i=clicked.property("myCol")

		# handles placing the flag
		if self.flag_selector == True:
			clicked.setStyleSheet(self.style_bomb)
			self.bomb_count -= 1
			self.bombs_remaning_label.setText("Bombs: " + str(self.bomb_count))
		
		else:
			# update bomb and move counter
			self.move_counter += 1
			self.move_counter_label.setText("Moves: " + str(self.move_counter))
			

			# if alive
			if self.current_model.bomb_located(row_i, col_i):
				clicked.setStyleSheet(self.style_bomb)
				return self.died()

			# Expand on button click
			self.current_model.expansion_handler(row_i, col_i)

			# update seen grid
			self.cur_model_uncovered_grid = self.current_model.get_uncovered_grid()

			# redraw grid layout 
			for i in range(self.row_n):
				for j in range(self.col_n):
					if self.cur_model_uncovered_grid[i][j] == '_': # if current square is showing           							
						single_index = i * self.row_n + j  				  # change button color 
						cur_btn = self.grid.itemAt(single_index).widget()
						cur_btn.setStyleSheet(self.style_pressed) 
						if self.cur_model_grid[i][j] != "0":
							cur_btn.setText(self.cur_model_grid[i][j])   # change button text to include bomb neighbors
		
		# check if player has won
		if self.current_model.has_won():
			self.has_won()
