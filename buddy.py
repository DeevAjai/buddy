import pyttsx3,os,sys

class  speech:
    def __init__(self):
        self.engine=pyttsx3.init()
        voices=self.engine.getProperty('voices')
        self.engine.setProperty('voice',voices[len(voices)-1].id)
    def speak(self,audio):
        print('LUCY:'+audio)
        self.engine.say(audio)
        self.engine.runAndWait()
    def user(self,name):
        self.speak('Hi '+name+',I am LUCY your personal assistant')
        rep=1
        while rep:
            sp=input('USER:')
            if (sp != 'bye') & (sp != ''):
                t=sp.split()
                for i in t:
                    if (i == 'open') | (i == 'read'):
                        self.speak('Choose file name to read:')
                        lis=os.listdir()
                        for i in lis:
                            self.speak(i)
                        fn=input()
                        self.file(fn,'r')
                        sp=''
                    elif i == 'write':
                        self.speak('Write a file name:')
                        fn=input()
                        self.file(fn,'w')
                        sp=''
                    self.speak('How can i help you?')
            elif sp == 'bye':
                self.speak('bye '+name)
                rep=0
        self.engine.stop()
    def file(self,name,typ):
        f=open(name,typ)
        if typ == 'r':
            self.speak(f.read())
        elif typ == 'w':
            self.speak('Type your text')
            txt=input()
            f.write(txt)
        f.close()

if __name__=='__main__':
    a=input('Enter your name:')
    s=speech()
    s.user(a)
    sys.exit()
        
