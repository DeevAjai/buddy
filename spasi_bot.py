import os,re,time
import aiml,requests
from gtts import gTTS,gTTSError
from playsound import playsound,PlaysoundException
import speech_recognition as sr

class Speech:
	def __init__(self):
		self.Voicefolder=os.path.abspath("./bot_data/voicenotes")
		self.flag=self.check_connection()
		self.mode=False
		self.r=sr.Recognizer()
		self.mic=sr.Microphone()
		#print("check_connection")
		if os.path.exists(self.Voicefolder):
			pass
		else:
			os.makedirs(self.Voicefolder)
		"""start=gTTS(text='Activated voice system',lang='en-in')
		a='activation.mp3'
		start.save(a)"""

	def check_connection(self):
		try:
			req=requests.get("https://www.google.com/",timeout=5)
			return True
		except requests.ConnectionError as e:
			print("No Network found")
			return False

	def talk(self,file):
		print("talking")
		def check_audio(audio):
			if os.path.exists(audio):
				try:
					playsound(audio)
				except PlaysoundException:
					os.remove(audio)
			elif self.flag:
				try:
					voice=gTTS(text=file,lang="en-in")
					voice.save(audio)
					playsound(audio)
				except gTTSError:
					self.flag=False
					self.talk("Network Error")
				except PlaysoundException:
					os.remove(audio)
			'''if not self.flag:
				os.remove(audio)'''
		check_audio(os.path.join(self.Voicefolder,re.search("[a-zA-Z0-9 ]+",file).group()+".mp3"))
		#self.bot_reply(file)
	
	def hear(self):
		with self.mic as source:
			self.r.adjust_for_ambient_noise(source);print("speak")
			audio = self.r.listen(source);print("listerned successfully")
			try:
				print("try block")
				text=r.recognize_google(audio);print("text recognised")
				return text
			except Exception as e:
				print(e)


class Mybot(Speech):
	def __init__(self):
		super(Mybot,self).__init__()
		self.kernel = aiml.Kernel()
		if os.path.isfile("bot_brain.brn"):
			self.kernel.bootstrap(brainFile="bot_brain.brn")
		else:
			self.kernel.bootstrap(learnFiles="std_setup.aiml", commands="learn files")
			self.kernel.saveBrain("bot_brain.brn")
		#print("Mybot init")
		self.greeting("enter")
		#print("greeting")

	def greeting(self,typ):
		t=time.localtime().tm_hour
		if typ == "enter":
			if t>=5 and 12>t:
				self.bot_reply("Good Morning")
			elif t>=12 and 17>t:
				self.bot_reply("Good Afternoon")
			elif t>=17 and 5>t:
				self.bot_reply("Good Evening")

	def bot_msg(self, msg):
		return self.kernel.respond(msg)
		
	def reload(self):
		self.kernel.bootstrap(learnFiles="std_setup.aiml", commands="learn files")
		self.brainsave()
	
	def brainsave(self):
		self.kernel.saveBrain("bot_brain.brn")
	
	def kill(self):
		if os.path.isfile("bot_brain.brn"):
			os.remove("bot_brain.brn")
	
	def response(self, message):
		if message in ["quit", "exit", "bye"]:
			bot_response = self.bot_msg("bye")
		elif message == "save":
			self.brainsave()
		elif message == "reload":
			self.reload()
		elif message == "activate voice":
			self.flag = self.check_connection()
			self.mode = self.flag
			if self.flag:
				pass
			else:
				message = "voice failed"
		elif message == "deactivate voice":
			self.flag = False
			self.mode = False
		bot_response = self.bot_msg(message)
		return bot_response

	def bot_reply(self,msg):
		if self.mode:
			self.talk(msg)
		print("BOT".ljust(5, " ")+"<<:", msg)    
	
	def user_input(self):
		if self.mode:
			uinput=self.hear()
			print("USER".ljust(5, " ")+">>: "+uinput)
			return uinput
		return input("USER".ljust(5, " ")+">>: ")
	
def main():
	bot = Mybot()
	while True:
		message = bot.user_input() 
		bot_response = bot.response(message)
		bot.bot_reply(bot_response)
		if message in ["quit", "exit", "bye"]:
			break
	#bot.brainsave()

if __name__=="__main__":
	main()
	