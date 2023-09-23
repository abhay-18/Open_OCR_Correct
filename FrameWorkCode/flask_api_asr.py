# # import required module
# import speech_recognition as sr



# # explicit function to take input commands
# # and recognize them
# def takeCommandHindi():
		
# 	r = sr.Recognizer()
# 	with sr.Microphone() as source:
		
# 		# seconds of non-speaking audio before
# 		# a phrase is considered complete
# 		print('Listening')
# 		r.pause_threshold = 0.7
# 		audio = r.listen(source)
# 		try:
# 			print("Recognizing")
# 			Query = r.recognize_google(audio, language='hi-In')
			
# 			# for listening the command in indian english
# 			print("the query is printed='", Query, "'")
		
# 		# handling the exception, so that assistant can
# 		# ask for telling again the command
# 		except Exception as e:
# 			print(e)
# 			print("Say that again sir")
# 			return "None"
# 		return Query



# # Driver Code
		
# # call the function
# takeCommandHindi()


from flask import Flask, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
import io
from werkzeug.utils import secure_filename

app = Flask(__name__)

def convert_to_wav(audio_binary, input_format):
    # Convert audio to WAV format
    audio = AudioSegment.from_file(io.BytesIO(audio_binary), format=input_format)
    wav_data = audio.export(format="wav").read()
    return wav_data


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
            print("Say that again sir")
            return "None"
        return Query
    
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_endpoint():
    print(request.files)
    if "file" in request.files:
        print("YESSSSS")
    else:
        print("NOOOO")
    audio_data = request.files["file"]
    
    fileName = secure_filename(audio_data.filename)
    audio_data.save("../data/server_data/"+fileName)
    
    
    
    print(type(audio_data))
    input_format="ogg"
    
    # wav_data = convert_to_wav(audio_data, input_format)
    
    if not audio_data:
        return jsonify({'error': 'No audio data received'})

    # Perform speech recognition
    recognized_text = recognize_speech("../data/server_data/"+fileName)
    
    
    # recognized_text="hello"
    # return jsonify({'text': recognized_text})
    return recognized_text

if __name__ == '__main__':
    app.run(debug=True)