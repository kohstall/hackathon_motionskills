# Python program to translate
# speech to text and text to speech

import speech_recognition as sr
import pyttsx3
import openai
import time
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env file

# Load env variables from .env file
openai.api_key = os.getenv("CHATGPT_PRIVATE_KEY")
messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

# Initialize the recognizerWhat
r = sr.Recognizer()

# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    engine.stop()

def outputSpeech2File(mText):
    # Open function to open the file "MyFile1.txt"
    # (same directory) in append mode and
    fhandle = open('SpeechOutput.txt','a')
    # fhandle.write('this is a test')
    fhandle.write(mText)
    fhandle.write('\n')
    fhandle.close()

def txt2Speech (text):
    engine = pyttsx3.init()
    engine.say(text)
    # engine.say(text1)
    engine.runAndWait()
    engine.stop()

def intro ():
    txt2Speech("Hi. I am Me Me. I am a smart robot.")

##########################################################
# main loop
# Loop infinitely for user to
# speak
##########################################################

# Welcome speech
intro()

count = 1
while(count):

    count = count-1

    # Exception handling to handle
    # exceptions at the runtime
    try:

        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            #listens for the user's input
            audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            print("Did you say ",MyText)
            SpeakText(MyText)

            # Save speech to text file
            outputSpeech2File(MyText)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")


# ChatGPT sub-section
messages = [ {"role": "system", "content":  "You are a intelligent assistant."} ]

chatgptCount = 1
while chatgptCount:
    chatgptCount = chatgptCount - 1

    # message = input("User : ")
    fhandle = open('SpeechOutput.txt')
    for line in fhandle:
        if line:
            messages.append(
                {"role": "user", "content": line},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
        reply = chat.choices[0].message.content
        print(f"ChatGPT: {reply}")
        messages.append({"role": "assistant", "content": reply})

        # TTS: ChatGPT reply to speech
        txt2Speech(reply)

        # sleep 1-2 secs
        # t = 1
        # time.sleep(t)

