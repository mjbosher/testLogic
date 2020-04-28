import os
from datetime import datetime
import random
import sys
from google_speech import Speech
import itertools
import urllib
from optparse import OptionParser 
from googletrans import Translator
import subprocess

path = os.getcwd()
log = f'{path}/../Log/log'
errorfile = f'{path}/../_Errors'

languages = {'R':'ru','E':'en','U':'uk'}
#dont forget to add to automake languages

options = OptionParser()
options.add_option('--audio','-a',dest='audio',help='audio')
options.add_option('--auto',dest='auto')
options.add_option('--version',dest='version')
options.add_option('--vcheck',dest='vcheck')
sound = ''
opts,x=options.parse_args()
audio = opts.audio
automake = opts.auto
version = opts.version
vcheck = opts.vcheck
if vcheck == 'True':
	print('Last updated 28/04/20')
	sys.exit()
if version == 'True':
	print(f'THIS COPY: Last updated 28/04/20' )
	print(f'MAIN COPY: {str(subprocess.check_output(["python3", "/home/michael/Local/PROJECTS/Review/_review.py", "--vcheck", "True"]))}')
	sys.exit() 
if audio == 'off':
	sound = 'off'
else:
	try:
		urllib.request.urlopen('http://www.yahoo.co.uk') 
		sound = 'on'	
	except IOError:
		print('NO INTERNET CONNECTION\n')
		sound = 'off'
		

if os.path.exists(log):
	pass
elif os.path.exists(log) == False:
	dirpath = log.rsplit('/',1)[0]
	command = (f'mkdir -p {dirpath}; touch {log}')
	os.system(command)
	print(f'CREATED LOG AT {log}')

class autoMake:
	languages_ = {'russian':['ru','R'],'ukrainian':['uk','U']}
	if len(sys.argv) > 1 and sys.argv[1] == '@make':
		if os.path.exists(sys.argv[2]):
			src = sys.argv[2]
			dest = sys.argv[3]
	
			data = [x.rstrip() for x in open(src)] 
			if automake:
				if data[0].lower().startswith('language'):
					if data[0].lower().split(':')[1] in languages_.keys():
						lang = languages_[data[0].lower().split(':')[1]][0]
						prefix = languages_[data[0].lower().split(':')[1]][1]
						data.pop(0)
						filedata=[]
						for i in data:
							word = i
							i = Translator().translate(i,src='en', dest=lang)
							if lang == 'ZH-cn':
								i.pronunciaton
							else:
								i=i.text
							x1 = f'{i.lower()}#{prefix}:{word.capitalize()}'
							x2 = f'{prefix}:{word.capitalize()}#{i.lower()}'
							filedata.append(x1)
							filedata.append(x2)
						
			else:
				data1 = [f'{x.split("#")[1]}#{x.split("#")[0]}' for x in data]
				filedata = []
				for x1,x2 in zip(data,data1):
					filedata.append(x1)
					filedata.append(x2)
			if os.path.exists(dest):
				overwrite = input('FILE EXISTS: OVERWRITE (y/n): ')
				if overwrite == 'y':
					os.remove(dest)
				else:
					raise IOError('File exists')
			os.mknod(dest)
			f = open(dest,'a')
			for i in filedata:
				f.write(f'{i}\n')
			f.close()
			print(f'FILE {dest} CREATED FROM {src}')

class Test:
	def __init__(self,file):
		self.file = file
		self.points = 0
		self.errs=set()
		if os.path.exists(self.file) or self.file.split('/')[-1] == '@mixed':
			if self.file.split('/')[-1] == '@mixed':
				self.file = '@mixed'
			print(f'OPENING {self.file} \n ')
			self.Process_file()
			self.Score()
		elif os.path.exists(self.file) == False and self.file !='@mixed':
			raise IOError(f' {file} DOES NOT EXIST \n')
		elif self.file == 'all':
			self.Concat()
			self.Score()
	def Process_file(self):
		if self.file == '@mixed':
			data = []
			if os.path.isdir('COMPLETE'):
				filepath = 'COMPLETE'
			else:
				filepath = '../COMPLETE'
			for x,f,d in os.walk(filepath):
				for i in d:
					lines = [x.strip() for x in open(os.path.join(x,i))]
					data.append(lines)
			lines = list(itertools.chain.from_iterable(data))
			n = int(input('Number of questions: '))
			lines = list(random.sample(lines,n))
		else:
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

		if len(question.split(':')) == 1 and len(answer.split(':')) > 1 and sound == 'on':
				speak=Speech(question,languages[answer.split(':')[0]])
				speak.play()
		elif len(question.split(':')) == 1 and len(answer.split(':')) == 1 and sound == 'on':
				speak=Speech(question,languages['E'])
				speak.play()
		elif len(question.split(':')) > 1 and sound == 'on':
				speak=Speech(question.split(':')[1],languages['E'])
				speak.play()

		while x != answer or x != 'Show':
			print('\n'+ question + '\n')
			x = input('YOUR ANSWER: ')
			if x == answer and y <= 3:
				self.points += 1
				if len(question.split(':')) > 1 and sound == 'on':
					speak=Speech(answer,languages[question.split(':')[0]])
					speak.play()
				elif len(answer.split(':')) > 1 and sound == 'on':	
					speak=Speech(answer.split(':')[1],languages['E'])
					speak.play()
				elif sound == 'on':	
					speak=Speech(answer,languages['E'])
					speak.play()
				break;
			elif x != answer and y > 3:
				error = '#'.join([answer,question])
				self.errs.add(error)
				break;
			elif x == 'Show':
				if len(question.split(':')) > 1 and sound == 'on':
					speak=Speech(answer,languages[question.split(':')[0]])
					speak.play()
				elif len(answer.split(':')) > 1 and sound == 'on':	
					speak=Speech(answer.split(':')[1],languages['E'])
					speak.play()
				elif sound == 'on':	
					speak=Speech(answer,languages['E'])
					speak.play()
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
		print('\n')
		for i in os.listdir(os.getcwd()):
			if not i.endswith('py') and i.startswith('_'):
				print(i)
		print('\n')
		if len(sys.argv) ==1:
			file = input('FILENAME: ')
			
		elif len(sys.argv) >= 2 and sys.argv[1].startswith('--audio'):
			file = input('FILENAME: ')
		elif len(sys.argv) >= 2:
			file = sys.argv[1]
		if file == '@make':
			autoMake()
			return(None)
		else:
			file = '/'.join([path,file])
		return(cls(file))

def main():
	init = Test
	init.File()	

if __name__ == "__main__":
	main()
'''
ADDED SPEECH DETECTS WHICH LANGUAGE FROM ANALYSING STRING
GIVES OPTION FOR --audio IF 'off' TURNS OFF SOUND OR IF NO INTERNET CONNECTION
ALSO ALLOWS TO ADD FILE AS SECOND ARG EG. 'python3 _review.py file --audio off'
ADDED @mixed which can be inputed as a file to get a random sample from COMPLETE or ../COMPLETE
ADDED @make which takes a src file to read from and a destination file, converts a list of words to a format suitable for this
can be used with --auto True to make a file from a list of words that dont have the foreign words alongside them
however on the top of the file must be a header with required language to translate to such as language:Russian
example useage of @make (python3 _review.py @make infile outfile --auto True)
'''
#maybe do other things like write what you hear without any words or write the responses to questions
#need to make markov generator
#in real _review.py need to include language and things as a header of the files that it reads
#also need to change the way it checks answers by adding the words into a list and having them checked without punctuation marks or caps
#added option to check version
