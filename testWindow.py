from PyQt5.QtWidgets import QFrame,QLabel,QGridLayout,QLineEdit,QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import random

class QuestionWindow(QFrame):
	def __init__(self,app):
#do stats,fix layout, add corrret questions, commit
		super().__init__()
		self.app = app
		self.question_window=QFrame()
		self.question_window.setStyleSheet('background:white')

		self.questionLabel = QLabel('')
		self.questionLabel.setText('hello')
		self.questionLabel.setFont(QFont('Ubuntu',20))
		self.questionLabel.setStyleSheet('color:red')

		self.questionLabel.setAlignment(Qt.AlignCenter|Qt.AlignVCenter)
		self.currentQuestionNumber,self.questionCorrect, self.questionWrong=QLabel(''),QLabel(''),QLabel()

		self.currentQuestionNumber.setFont(QFont('Ubuntu',13))
		self.currentQuestionNumber.setStyleSheet('color:blue')

		self.questionCorrect.setFont(QFont('Ubuntu',13))
		self.questionCorrect.setStyleSheet('color:green')
		
		self.questionWrong.setFont(QFont('Ubuntu',13))
		self.questionWrong.setStyleSheet('color:red')
		
		self.wrongAnswerLabel=QLabel('')
		self.wrongAnswerLabel.setFont(QFont('Ubuntu',13))
		
		self.answerLabel=QLabel('')
		self.answerLabel.setFont(QFont('Ubuntu',13))
		self.answerLabel.setStyleSheet('color:red')

		self.answerBox = QLineEdit()
		self.checkAnswer = QPushButton('Check Answer')
		self.answerBox.setStyleSheet('color:blue')
		self.answerBox.setFrame(1)
	
		grid = QGridLayout()
		self.question_window.setLayout(grid)
		
		grid.addWidget(self.currentQuestionNumber,0,0)
		grid.addWidget(self.questionCorrect,0,2,1,1)
		grid.addWidget(self.questionWrong,0,3,1,1)
		
		grid.addWidget(self.questionLabel,1,0,10,4)
		grid.addWidget(self.wrongAnswerLabel,11,0,1,2)
		grid.addWidget(self.answerBox,12,0,1,3)

		grid.addWidget(self.answerLabel,11,1,1,1)
		grid.addWidget(self.checkAnswer,12,3)

	def statsFrame(self):
		x=QFrame()
		self.app.setCentralWidget(x)
		grid = QGridLayout()
		x.setLayout(grid)	
		x.setStyleSheet('background:blue')		
		

class testLogic(QuestionWindow):
	def __init__(self,app,file):
		super().__init__(app)
		
		self.correctAnswersPercent = 0
		self.wrongAnswersPercent = 0
		self.correctAnswers = 0
		self.wrongAnswers = 0
		self.checkAnswer.clicked.connect(lambda:self.check_answer(0))
		self.errors = []
		self.file = file
		self.data = [x.rstrip() for x in open(self.file) if x != '\n']
		self.questionNumber = 0
		self.totalQuestions = len(self.data)
		self.pointStep = 100/self.totalQuestions 
		self.parseData()
		
		#need to writeout self.errors
	def parseData(self):
		if len(self.data) != 0:
			self.questionNumber+=1
			self.origData = random.choice(self.data)
			splitData = self.origData.split('#')
			self.answer = splitData[0]
			self.question = splitData[1]
			self.askQuestion(self.question,self.answer)
			self.tries = 0
			self.wrongAnswerLabel.setText('')
			self.data.remove(self.origData)
		else:
			self.question_window.close()
			self.statsFrame()
	def check_answer(self,x):
		
		userInput = self.answerBox.text()
		if self.tries == 2:
			self.answerLabel.setText(f'ANSWER IS: {self.answer} ')
			self.errorCollector(self.origData)
			self.wrongAnswersPercent+=self.pointStep
			self.wrongAnswers+=1
			self.checkAnswer.setText('Next')
			self.tries+=1
		elif self.tries ==3:
			self.parseData()
			self.answerBox.clear()
			self.checkAnswer.setText('Check Answer')
			self.answerLabel.setText('')
		elif userInput == self.answer:
			self.correctAnswersPercent+=self.pointStep
			self.correctAnswers+=1
			self.parseData()
			self.answerBox.clear()
		else:
			colors=['green','blue','red','purple']
			color =random.choice(colors)
			colors.remove(color)
			
			self.askQuestion(self.question,self.answer)
			self.tries+=1
			self.wrongAnswerLabel.setText('wrong answer: try again')
			self.wrongAnswerLabel.setStyleSheet(f'color:{color}')
			self.answerBox.clear()

	def askQuestion(self,q,a):
		self.currentQuestionNumber.setText(f'Question: {self.questionNumber} of {self.totalQuestions}')
		self.questionCorrect.setText(f'correct: {self.correctAnswers} ({round(self.correctAnswersPercent)}%)')
		self.questionWrong.setText(f'wrong: {self.wrongAnswers} ({round(self.wrongAnswersPercent)}%)')
		self.questionLabel.setText(q)
		#write current number of right/wrong questions
		
		
	def errorCollector(self,error): 
		self.errors.append(error)
	def complete(self):
		return(self.file, self.correctAnswers, self.wrongAnswersPercent, self.wrongAnswers, self.wrongAnswersPercent, self.error)
#estLogic('_data-measurement')
