from PyQt5.QtWidgets import (QApplication,QGridLayout,QDesktopWidget,QMainWindow,QFrame)
import sys
from fileMenu import FileMenu
from testWindow import testLogic

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		maingrid = QGridLayout()
		qframe = testLogic(self,'/home/michael/Downloads/Workarea/DevLearn/Linux/COMPLETE/_Basics1').question_window
		
			
		#to be done later
		#FileMenu(self)
		#--------------
		
		self.setCentralWidget(qframe)
		#self.setLayout(maingrid)
		self.resize(1000,600)
		self.__adjust__()
		self.show()

	def __adjust__(self):
		window = QDesktopWidget().availableGeometry()
		window = window.center()
		frame = self.frameGeometry()
		frame = frame.center()
		self.move(window-frame)



if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = App()
	sys.exit(app.exec_())
	
