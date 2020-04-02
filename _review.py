import os
from datetime import datetime
import random
path = os.getcwd()
log = f'{path}/../Log/log'
errorfile = f'{path}/../_Errors'

print('\n')
for i in os.listdir(os.getcwd()):
	if not i.endswith('py') and i.startswith('_'):
		print(i)
print('\n')

if os.path.exists(log):
	print('LOG EXISTS \n ')
elif os.path.exists(log) == False:
	dirpath = log.rsplit('/',1)[0]
	command = (f'mkdir -p {dirpath}; touch {log}')
	os.system(command)
	print(f'CREATED LOG AT {log}')

class Test:
	def __init__(self,file):
		self.file = file
		self.points = 0
		self.errs=set()
		if os.path.exists(self.file):
			print(f'OPENING {self.file} \n ')
			self.Process_file()
			self.Score()
		elif os.path.exists(self.file) == False and self.file != 'all':
			raise IOError(f' {file} DOES NOT EXIST \n')
		elif self.file == 'all':
			self.Concat()
			self.Score()
	def Process_file(self):
		lines = [x.strip() for x in open(self.file)]
		self.total = int(len(lines))
		x = 0
		while x < self.total:
			q = x+1
			print(f'\nQuestion {q}/{self.total}\n')
			line = random.choice(lines)
			newline = line.split('#')
			answer = newline[0]
			question = newline[1]
			self.test(question,answer)
			lines.remove(line)
			x+=1
	def Concat(self):
		lines = set()
		for files in os.listdir(path):
			if files == '_instructions' or files == 'Log' or files == '_Errors' or files.endswith('py') or files.endswith('swp'):
				pass
			else:
				print(files)
				x = {l.strip() for l in open(files)}
				lines |= x
		self.total = int(len(lines))
		x = 0
		while x < self.total:
			q= x+1
			print(f'\nQuestion {q}/{self.total}\n')
			lines = list(lines)
			line = random.choice(lines)
			newline = line.split('#')
			answer = newline[0]
			question = newline[1]
			self.test(question,answer)
			lines.remove(line)
			x+=1

	def test(self,question, answer):
		x = ''
		y = 0
		while x != answer or x != 'Show':
			print('\n'+ question + '\n')
			x = input('YOUR ANSWER: ')
			if x == answer and y <= 3:
				self.points += 1
				break;
			elif x == answer and y > 3:
				error = '#'.join([answer,question])
				self.errs.add(error)
				break;
			elif x == 'Show':
				error = '#'.join([answer,question])
				self.errs.add(error)
				print('\n'+answer+'\n')
				break;
			elif x != answer:
				print('\nWRONG!!\n')
				y+=1
				continue;
	def Score(self):
		date = str(datetime.now()).rsplit(':',1)[0]
		print(f'DATE: {date}')
		try:
			file = self.file.rsplit('/',1)[1]
		except IndexError:
			file ='ALL'
		print(f'FILE: {file}')
		print(f'SCORE: {self.points}/{self.total}')
		percent = self.total / 100
		score = self.points / percent
		score = round(score)
		print(f'PERCENT: {score}%')
		line = (f'\n{date} {file} {score}%')
		f=open(log,'a')
		f.write(line)
		f.close()
		if os.path.exists(errorfile) and self.file != errorfile:
			posterrors={x.strip('\n') for x in open(errorfile)}
			self.errs |= posterrors
		elif os.path.exists(errorfile) and self.file == errorfile:
			os.remove(errorfile)
			os.mknod(errorfile)
		elif os.path.exists(errorfile) == False:
			os.mknod(errorfile)
		f = open(errorfile,'w')
		for i in self.errs:
			f.write(i+'\n')
		f.close()
		print(len(list(self.errs)))			
	@classmethod
	def File(cls):
		file = input('FILENAME: ')
		if file == 'all':
			file = 'all'
		else:
			file = '/'.join([path,file])
		return(cls(file))

def main():
	init = Test
	init.File()	

if __name__ == "__main__":
	main()
