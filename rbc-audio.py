#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import openai
from gtts import gTTS
import os
#import pandas as pd
import time
from pygame import mixer

OPENAI_API_KEY = "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"


def play(s) :
    mixer.init()
    mixer.music.load(s)
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)
    
def sayit(mytext):
    l="en"  # -GB-Neural2-B
    myobj = gTTS(text=mytext, lang=l, slow=False)
      
    # Saving the converted audio in a mp3 file named
    myobj.save("rbc.mp3")
      
    # Playing the converted file
    play("rbc.mp3")   

def get_completion(prompt, model="gpt-4"):

    messages = [{"role": "system", "content" : "you are a helpful robot called Ash"},
                {"role": "user",   "content" : prompt}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


# obtain audio from the microphone
r = sr.Recognizer()
sayit("Hello")
while True:   
    with sr.Microphone() as source:
        print(">> ")
        audio = r.listen(source)
   
        # recognize speech using Whisper API

        try:
            openai.api_key=OPENAI_API_KEY
            prompt = r.recognize_whisper_api(audio, api_key=OPENAI_API_KEY)
            print(f"'{prompt}'")  
            
            if prompt=="Bye." or prompt=='. .' :
                sayit("Good bye")
                break
                
            if prompt=="." :
                continue
                
            response = get_completion(prompt)
            print(response)
                       
            # The text that you want to convert to audio
            sayit(response)
              

        except sr.RequestError as e:
            print("Could not request results from Whisper API")
    
        
