from flask import Flask, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
import io
from werkzeug.utils import secure_filename
import pydub
import wave
import os

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




# Function to recognize speech
def recognize_speech(audio_file_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        r.pause_threshold = 0.7
        audio = r.listen(source); print(type(audio))
        try:
            print("Recognizing")
            Query = r.recognize_google(audio, language='hi-In')
            print("the query is printed='", Query, "'")
        except Exception as e:
            print(e)
            print("Say that again")
            return "None"
        return Query
    
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_endpoint():
    print(request)
    if "file" in request.files:
        print("YES")
    else:
        print("NO")
        return "False"
    audio_data = request.files["file"]
    convertFlactoWav(audio_data)
    # print(audio_data)
    # # wav_data = convert_to_wav(audio_data, input_format)
    # fileName = secure_filename(audio_data.filename)
    # print(fileName)
    # # fileName = secure_filename(wav_data.filename)
    # audio_data.save("../data/server_data/"+fileName)
    # audio_data.save("../data/server_data/output.wav")
    # if audio_data.filename.endswith('.flac'):
    #     # Convert FLAC to WAV
    #     audio = AudioSegment.from_file(audio_data, format='flac')
    #     wav_data = audio.export(format='wav')

    #     # Save the WAV file
    #     wav_file_path = '../data/server_data/output.wav'
    #     wav_data.export(wav_file_path, format='wav')

    #     return jsonify({'message': 'Conversion and saving successful'})
    
    if not audio_data:
        return jsonify({'error': 'No audio data received'})

    # Perform speech recognition
    recognized_text = recognize_speech("../../data/server_data/output.wav")
    
    # recognized_text="hello"
    # return jsonify({'text': recognized_text})
    return recognized_text

if __name__ == '__main__':
    app.run(debug=True)