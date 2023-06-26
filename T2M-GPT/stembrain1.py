
import serial
import numpy as np
import time

from quickstart import Model

import re


import main as speech_module

import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write



class Spine():

    def __init__(self, port='/dev/ttyACM0', baud_rate=1000000):
        try:
            self.ser = serial.Serial(port, baud_rate)
        except:
            print('ERROR: Spine could not be connected')

    def communicate(self, commands):
        
        commands_package = bytes(commands.astype(dtype=np.int8))
        #print('writing', commands_package, 'to spine')
        self.ser.write(commands_package)

        # --- Receive readings
        #print('bytes available',self.ser.in_waiting)
        if self.ser.in_waiting:

            readings_bytes = self.ser.read(8)

            # --- CHECK for more stuff in buffer and empty it
            while self.ser.in_waiting:
                self.ser.read()
                print("[readings] ERROR: extrabytes")

            # --- DECODE readings

            readings_raw = np.frombuffer(readings_bytes, dtype=np.uint8)
            return readings_raw
        else:
            return -1


def run_cmd(i_out, time_scale=0.035):
    commands = np.array([i_out[2], i_out[0], i_out[1]+30, 8], dtype=np.int16)
    spine.communicate(commands)
    time.sleep(time_scale)

if __name__=="__main__":
    spine = Spine()
    commands = np.array([0, 00, 0, 8], dtype=np.int16)

    model = Model()


    speech_module.intro()

    while True:
        readings = spine.communicate(commands)
        

        print("Bot now listening")

        txt = speech_module.listen()

        if not txt.strip():
            # reply = 'Sorry, your command was not understood.'
            speech_module.txt2Speech("Please say something.")

            continue
        
        #txt = input("Enter text here: ")

        #txt = "a person is waving"


        print("Sending to OpenAI:", txt)

        reply = speech_module.openai_reply(txt)

        print("OpenAI Reply", reply)

        try:
            test =  reply.split('[action]') 

            print(test, "SDFSDF")

            sentence_to_say, command, *_ = test
            print("Should sentence_to_say 1!", sentence_to_say)

            sentence_to_say = re.sub("\[.*\]", "", sentence_to_say)

            command = command.replace("*", "")

            # get first sentence from command
            if "." in command:
                command = command[:command.find('.')]
            
            if "!" in command:
                command = command[:command.find('!')]

            # if "-" in command:
            #     command = command[:command.find('-')]

            print("Should act!", command)
            arm_coords = model.inference([command])[0]


            print("Should sentence_to_say!", sentence_to_say)
            speech_module.txt2Speech(sentence_to_say)

            out = []
            for i in arm_coords:
                out.append(i[-1] - i[0])


            out_scaled = (np.array(out)*100) + 50 

            for num_times in range(3):
                i_last = np.zeros([3])
                first_point = True

                for i in out_scaled:
                    if first_point:
                        i_last = i
                        first_point = False
                    # print(i)

                    i_out = (i + i_last)/2

                    print(i_out)
                    run_cmd(i_out)

                    i_out = i
                    print(i_out)
                    run_cmd(i_out)

                    i_last = i

            print(out_scaled[0], out_scaled[-1], "first and last")

        except ValueError:
            # speech_module.txt2Speech('Sorry, your command was not understood.')
            speech_module.txt2Speech(reply)
        else:
            speech_module.txt2Speech("How can I help?")

        # print(out)
        print('main readings', readings)
        time.sleep(0.3)


        # break