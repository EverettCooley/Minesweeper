from MineModel import *
from MineView import *
import sys

# arguments to be pass through
grid_size=sys.argv[1]
bomb_count=sys.argv[2]

app = QApplication([])
mainWindow = MainWindow(gird_size, bomb_count)
mainWindow.show()
app.exec_()