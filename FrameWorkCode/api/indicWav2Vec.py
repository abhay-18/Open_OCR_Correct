from flask import Flask, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
import io
from werkzeug.utils import secure_filename
import pydub
import wave
import os


def recognize_speech(audio_file_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        r.pause_threshold = 0.7
        audio = r.listen(source); print(type(audio))
        try:
            print("Recognizing")
            Query = r.recognize_google(audio, language='ta-In')
            print("the query is printed='", Query, "'")
        except Exception as e:
            print(e)
            print("Say that again")
            return "None"
        return Query
    
recognized_text = recognize_speech("/home/abhay/Downloads/tamil.wav")
print(recognized_text)
