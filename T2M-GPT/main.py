# Python program to translate
# speech to text and text to speech

import speech_recognition as sr
import pyttsx3
import openai
import time
import os
from gtts import gTTS
import playsound


from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env file

# Load env variables from .env file
openai.api_key = os.getenv("CHATGPT_PRIVATE_KEY")
messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

# Initialize the recognizerWhat
r = sr.Recognizer()



engine = pyttsx3.init()


rate = engine.getProperty('rate')   # getting details of current speaking rate
print ("Rate", rate)                   
engine.setProperty('rate', 125)     # setting up new voice rate

voices = engine.getProperty('voices')

print("Voices", voices)
engine.setProperty('voice', voices[11].id)



# Function to convert text to
# speech
def SpeakText(command):

    engine.say(command)
    engine.runAndWait()
    engine.stop()

def outputSpeech2File(mText):
    # Open function to open the file "MyFile1.txt"
    # (same directory) in append mode and
    fhandle = open('UserOutput.txt','a')
    # fhandle.write('this is a test')
    fhandle.write(mText)
    fhandle.write('\n')
    fhandle.close()

def txt2Speech (text):
    # engine.say(text)
    # engine.runAndWait()
    # engine.stop()


    # Language in which you want to convert
    language = 'en'
    
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=text, lang=language, slow=False)

    myobj.save("temp.mp3")

    playsound.playsound('temp.mp3')



def intro ():
    txt2Speech("Hi. I am Moo Me. How can I help?")

##########################################################
# main loop
# Loop infinitely for user to
# speak
##########################################################

def listen():

    MyText = ""

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
            audio2 = r.listen(source2, timeout=5, phrase_time_limit=5)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            # print("Did you say ",MyText)
            # SpeakText(MyText)

            # Save speech to text file
            outputSpeech2File(MyText)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")

    return MyText


def openai_reply(txt):
#     # ChatGPT sub-section
    messages = [ {"role": "system", "content":  '''You are a robot. You can move your right arm only.
The user will ask you to do something.
You will respond with an action and by saying something funny.

Your response must include "person" and "right arm".

For example:

User: "wave your hand"
You: "[speak] Waving like I can't stop waving [action] person waving the right arm"

User: "point forward"
You: "[speak] Pointing at something random in front of me [action] person pointing right arm forward"

User: "dance for us"
You: "[speak] Let's have a dance party [action] person making dance moves with right arm"

User: "punch the air repeatedly"
You: "[speak] I'm going to punch the air until I get tired, or until my arm falls off [action] person punching air repeatedly with right arm"

User: "pump your fist in the air"
You: "[speak] Let's go! [action] person pumping right arm in the air"'''} ]

#     messages = [ {"role": "system", "content":  '''You are a robot. You can move your right arm only.
# The user will ask you to do something.
# You will respond with an action and saying something funny.
# For example:

# User: "wave your hand"
# You: "[speak] Waving like I can't stop waving [action] person waving the right arm"
# User: "point forward"
# You: "[speak] Pointing at something random in front of me [action] person pointing right arm forward"
# User: "dance for us"
# You: "[speak] Let's have a dance party [action] person making dance moves with right arm"'''} ]

    messages.append({"role": "user", "content": txt})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0
    )

    reply = chat.choices[0].message.content
    
    print(f"ChatGPT: {reply}")

    # # TTS: ChatGPT reply to speech
    # txt2Speech(reply)

    return reply


def main():
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

                # print("Did you say ",MyText)
                # SpeakText(MyText)

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

