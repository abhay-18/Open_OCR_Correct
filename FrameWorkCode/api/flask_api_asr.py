from flask import Flask, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
import io
from werkzeug.utils import secure_filename
import pydub
import wave
import os
import requests
import time

app = Flask(__name__)


def convertFlactoWav(flac_data):
    # Read the FLAC data into a BytesIO object
    flac_io = io.BytesIO(flac_data.read())

    # Load the FLAC audio from the BytesIO object
    audio = AudioSegment.from_file(flac_io, format="flac")

    # Export the audio as WAV to another BytesIO object
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")

    # Get the WAV data as bytes
    wav_bytes = wav_io.getvalue()
    
    output_directory = "../../data/server_data/"
    output_file_name = "output.wav"

    # Create the full path for the output file
    output_file_path = os.path.join(output_directory, output_file_name)

    # Write the WAV data to the file
    with open(output_file_path, "wb") as wav_file:
        wav_file.write(wav_bytes)
    # Now, 'wav_bytes' contains the WAV audio data
    print("file converted from flac to wav!!!!!!!!")


def recognize_sanskrit(audio_file_path):
    API_URL = "https://api-inference.huggingface.co/models/Harveenchadha/vakyansh-wav2vec2-sanskrit-sam-60"
    headers = {"Authorization": f"Bearer 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"}

    with open(audio_file_path, "rb") as f:
        data = f.read()

    response = requests.post(API_URL, headers=headers, data=data)

    while 'error' in response.json() and 'estimated_time' in response.json():
        print(f"Model still loading. Waiting for {response.json()['estimated_time']} seconds.")
        time.sleep(10)
        response = requests.post(API_URL, headers=headers, data=data)

    output = response.json()
    print(output)
    result = output['text']
    print(result)
    result=result.replace("<s>", '')
    return result


# Function to recognize speech
def recognize_speech(audio_file_path, lang):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        r.pause_threshold = 0.7
        audio = r.listen(source); print(type(audio))
        try:
            print("Recognizing")
            Query = r.recognize_google(audio, language=f'{lang}-In')
            print("the query is printed='", Query, "'")
        except Exception as e:
            print(e)
            print("Say that again")
            return "None"
        return Query


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_endpoint():
    # print(request)
    # print(request.files)
    lang = request.form.get('lang')
    # print(lang)
    if "file" in request.files:
        print("YES")
    else:
        print("NO")
        return "False"
    audio_data = request.files["file"]
    convertFlactoWav(audio_data)
    
    if not audio_data:
        return jsonify({'error': 'No audio data received'})

    # # Perform speech recognition
    recognized_text = ""
    if lang == "sn": 
        recognized_text = recognize_sanskrit("../../data/server_data/output.wav")
    
    else:
        recognized_text = recognize_speech("../../data/server_data/output.wav", lang)
    # recognized_text="hello"
    # return jsonify({'text': recognized_text})
    return recognized_text

if __name__ == '__main__':
    app.run(debug=True)