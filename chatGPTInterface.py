import openai
import time
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

private_key = os.getenv("CHATGPT_PRIVATE_KEY")
print(private_key) # for testing purposes only

# openai.api_key = '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'
# openai.api_key = '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'
# openai.api_key = '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'
messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

chatgptCount = 0
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

        # sleep 1-2 secs to prevent OpenAI filter
        t = 1
        time.sleep(t)

