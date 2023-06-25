# Python program to translate
# speech to text and text to speech

import speech_recognition as sr
import pyttsx3
import openai

# openai.api_key = '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'
openai.api_key = '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'
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

def outputSpeech2File(mText):
    # Open function to open the file "MyFile1.txt"
    # (same directory) in append mode and
    fhandle = open('SpeechOutput.txt','a')
    # fhandle.write('this is a test')
    fhandle.write(mText)
    fhandle.write('\n')
    fhandle.close()


# Loop infinitely for user to
# speak

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
            # Save speech to text
            # outputSpeech2File(MyText)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")

# import openai
# openai.api_key = 'YOUR_API_KEY'
# messages = [ {"role": "system", "content":  "You are a intelligent assistant."} ]

while True:
    message = input("User : ")
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})
