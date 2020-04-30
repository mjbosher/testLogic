from PyQt5.QtWidgets import QFrame,QLabel,QGridLayout,QLineEdit,QPushButton,QScrollBar
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import Qt,QSize
import random

class QuestionWindow(QFrame):
	def __init__(self,app):
#do stats,fix layout, add corrret questions, commit
#stop lineedit from resizing,make text bigger, 
#fix bugs ith error messages
#what is combo box, groupbox
#i think there is an extra click in the answerbox that doesnt register whether the answrr is right or not
		super().__init__()
		self.app = app
		self.question_window=QFrame()
		self.question_window.setFixedSize(1000,600)		
		grid = QGridLayout()
		self.question_window.setLayout(grid)

		
		self.currentQuestionNumber=QLabel('')
		self.questionCorrect=QLabel('')
		self.questionWrong=QLabel('')
		self.questionLabel = QLabel('')
		self.wrongAnswerLabel=QLabel('')
		self.answerLabel=QLabel('')
		self.answerBox = QLineEdit()
		self.checkAnswer = QPushButton('')
	
		self.answerBox.setFocus(1)
		self.answerBox.setAlignment(Qt.AlignCenter)
		icon = QIcon('next.jpeg')

		self.checkAnswer.setIcon(QIcon(icon))
		self.checkAnswer.setIconSize(QSize(200,200))
		self.checkAnswer.setFixedSize(150,150)
		self.checkAnswer.setAttribute(Qt.WA_TranslucentBackground)
		self.questionLabel.setWordWrap(True)
		self.currentQuestionNumber.setFont(QFont('Ubuntu',13))
		self.questionCorrect.setFont(QFont('Ubuntu',13))
		self.questionWrong.setFont(QFont('Ubuntu',15))
		self.answerLabel.setFont(QFont('Ubuntu',17))
		self.wrongAnswerLabel.setFont(QFont('Ubuntu',13))
		self.questionLabel.setFont(QFont('Ubuntu',20))
		self.answerBox.setFont(QFont('Ubuntu',20))
		self.questionWrong.setStyleSheet('color:red')
	
		self.answerLabel.setStyleSheet('color:red')
		self.questionCorrect.setStyleSheet('color:green')
		self.currentQuestionNumber.setStyleSheet('color:blue')
		self.answerBox.setStyleSheet(
			'color:blue; border-width: 1px; border-style: solid; border-color: white white black white;')		
		self.question_window.setStyleSheet('background:white')
		self.questionLabel.setStyleSheet('color:red')
		self.checkAnswer.setStyleSheet('border:1px solid white;border-radius:50%')
			
		self.questionLabel.setAlignment(Qt.AlignCenter|Qt.AlignVCenter)

		self.answerBox.setFrame(1)
		self.answerLabel.setWordWrap(True)
		grid.addWidget(self.currentQuestionNumber,0,0)
		grid.addWidget(self.questionCorrect,0,2)
		grid.addWidget(self.questionWrong,0,4)
		
		grid.addWidget(self.questionLabel,1,1,2,3)
		grid.addWidget(self.wrongAnswerLabel,4,2,1,2)
		grid.addWidget(self.answerBox,3,1,1,3)

		grid.addWidget(self.answerLabel,5,2,1,1)
		grid.addWidget(self.checkAnswer,5,4)

class Stats:
	def statsFrame(self,testLogic):
		statFrame=QFrame()
		self.testLogic = testLogic
		self.testLogic.app.setCentralWidget(statFrame)
		self.grid = QGridLayout()

		statFrame.setLayout(self.grid)	
		statFrame.setStyleSheet('background:white')

		questionFrame = QFrame(statFrame)
		self.grid.addWidget(questionFrame,0,0,5,1)
		subgrid = QGridLayout()
		
		questionFrame.setLayout(subgrid)

		self.file = [x.rstrip() for x in open(self.testLogic.file)]
		
		self.labels = [QLabel(''),QLabel(''),QLabel(''),QLabel(''),QLabel(''),QLabel('')]
		
		for n,i in enumerate(self.labels): subgrid.addWidget(i,n,0)
		
		self.scrollbar = QScrollBar()
		maximum = int(len(self.file)/6)
		self.scrollbar.setMaximum(maximum)
		subgrid.addWidget(self.scrollbar,0,1,7,1)
		self.scrollbar.valueChanged.connect(lambda: self.Subset(self.scrollbar.value()))
		self.addlabels(self.file[0:6])
	def addlabels(self,subset):
		for n,i in enumerate(subset):
			self.labels[n].setText(i)
			if i in self.testLogic.errors:
				self.labels[n].setStyleSheet('color:red')
				
			else:
				self.labels[n].setStyleSheet('color:green')
			#y.setFixedHeight(20)
	def Subset(self,b):
		self.setDefault()
		start,stop=(b)*6,(b+1)*6
		if stop > len(self.file):
			stop = len(self.file)
		subset=self.file[start:stop]
		self.addlabels(subset)
		self.oldscroll_val = self.scrollbar.value()
		print(start,stop)
	def setDefault(self):
		[i.setText('') for i in self.labels]
		#split the answers and questions for display	
		#what happens if lens is not equal for example, lens here says 18 but actual lens is 14
		#fix clicked part of scroll bar
class testLogic(QuestionWindow):
	def __init__(self,app,file):
		super().__init__(app)
		self.file = file
		self.correctAnswersPercent = 0
		self.wrongAnswersPercent = 0
		self.correctAnswers = 0
		self.wrongAnswers = 0
		self.questionNumber = 1
		self.errors = []

		self.checkAnswer.clicked.connect(lambda:self.check_answer(0))
		self.answerBox.returnPressed.connect(lambda:self.check_answer(0))	
		self.data = [x.rstrip() for x in open(self.file) if x != '\n']
		self.totalQuestions = len(self.data)
		self.pointStep = 100/self.totalQuestions 

		self.parseData()
		
		#need to writeout self.errors
	def parseData(self):
		if len(self.data) != 0:
			
			self.origData = random.choice(self.data)
			self.answer,self.question = self.origData.split('#')
			self.askQuestion(self.question,self.answer)

			self.tries = 0
			self.questionNumber+=1

			self.wrongAnswerLabel.setText('')
			
			self.data.remove(self.origData)
		else:
			self.question_window.close()
			Stats().statsFrame(self)
		
	def askQuestion(self,q,a):
		
		self.currentQuestionNumber.setText(f'Question: {self.questionNumber} of {self.totalQuestions+1}')
		self.questionCorrect.setText(f'correct: {self.correctAnswers} ({round(self.correctAnswersPercent)}%)')
		self.questionWrong.setText(f'wrong: {self.wrongAnswers} ({round(self.wrongAnswersPercent)}%)')
		self.questionLabel.setText(q)
		self.answerBox.setFocus()	
	def check_answer(self,x):
		
		userInput = self.answerBox.text()
		if self.tries == 2:
			self.answerLabel.setText(f'ANSWER IS:\n {self.answer} ')
			self.errorCollector(self.origData)
			self.wrongAnswersPercent+=self.pointStep
			self.wrongAnswers+=1
			self.tries+=1
		elif self.tries ==3:
			self.parseData()
			self.answerBox.clear()
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
		
	def errorCollector(self,error): 
		self.errors.append(error)
	def complete(self):
		return(self.file, self.correctAnswers, self.wrongAnswersPercent, self.wrongAnswers, self.wrongAnswersPercent, self.error)


#date,time
