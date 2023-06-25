import pyttsx3

def txt2Speech (text):
    engine = pyttsx3.init()
    engine.say(text)
    # engine.say(text1)
    engine.runAndWait()

def intro ():
    txt2Speech("Hi. I am Me Me. I am a smart robot.")

# main routine
# engine = pyttsx3.init()
# text1 = readFromFile()
# engine.say("Hello hackers, welcome to our demo")
# engine.say(text1)
# engine.runAndWait()

# test prompt
txt2Speech("Hello hackers, welcome to our demo")
intro()
