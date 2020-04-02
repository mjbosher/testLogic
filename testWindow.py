from PyQt5.QtWidgets import QFrame,QLabel,QGridLayout,QLineEdit,QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import random

class QuestionWindow(QFrame):
	def __init__(self,app):
		super().__init__()
		self.question_window=QFrame()
		self.question_window.setStyleSheet('background:white')

		self.questionLabel = QLabel('')
		self.questionLabel.setText('hello')
		self.questionLabel.setFont(QFont('Ubuntu',20))
		self.questionLabel.setStyleSheet('color:red')
		self.questionLabel.setAlignment(Qt.AlignCenter|Qt.AlignVCenter)

		self.answerBox = QLineEdit()
		self.checkAnswer = QPushButton('Check Answer')
	
		grid = QGridLayout()
		self.question_window.setLayout(grid)
		grid.addWidget(self.questionLabel,0,0)
		grid.addWidget(self.answerBox,1,0)
		grid.addWidget(self.checkAnswer,1,1)
		
		

class testLogic(QuestionWindow):
	def __init__(self,app,file):
		self.correctAnswersPercent = 0
		self.wrongAnswersPercent = 0
		self.correctAnswers = 0
		self.wrongAnswers = 0

		self.errors = []
		self.file = file
		self.data = [x.rstrip() for x in open(self.file) if x != '\n']
		self.questionNumber = 0
		self.totalQuestions = len(self.data)
		self.pointStep = 100/self.totalQuestions 
		self.main()

		#need to writeout self.errors

	def main(self):
		while len(self.data) != 0:
			self.questionNumber+=1
			self.parseData()

	def parseData(self):
		origData = random.choice(self.data)
		splitData = origData.split('#')
		answer = splitData[0]
		question = splitData[1]
		tries = 0
		while tries != 3:
			userInput= self.askQuestion(question,answer)
			if tries == 2:
				print(f'ANSWER IS: {answer} ')
				self.errorCollector(origData)
				self.wrongAnswersPercent+=self.pointStep
				self.wrongAnswers+=1
				break;
			elif userInput == answer:
				self.correctAnswersPercent+=self.pointStep
				self.wrongAnswers+=1
			else:
				tries+=1
		self.data.remove(origData)

	def askQuestion(self,q,a):
		currentQuestionNumber = f'Question: {self.questionNumber} of {self.totalQuestions}'
		print(f'correct: {round(self.correctAnswersPercent)} %, wrong: {round(self.wrongAnswersPercent)} % \n')
		print(currentQuestionNumber,q,sep='||',end='\n')
		answer = input('Answer: ')
		if answer == a:
			return(answer)
	
	def errorCollector(self,error): 
		self.errors.append(error)
	def complete(self):
		return(self.file, self.correctAnswers, self.wrongAnswersPercent, self.wrongAnswers, self.wrongAnswersPercent, self.error)
#estLogic('_data-measurement')
