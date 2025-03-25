from flask import Flask, request, jsonify, send_file
from googletrans import Translator
import os
import random

app = Flask(__name__)
translator = Translator()

@app.route('/')
def index():
    return send_file('Translator.html')  # Ensure this file is in the same folder

@app.route('/translate')
def translate_word():
    word = request.args.get('word', '').strip()
    try:
        translated = translator.translate(word, src='en', dest='hi')
        hindi_text = translated.text

        # Build video file path (capitalize first letter)
        video_filename = f"{word.capitalize()}.mp4"
        video_path = f"static/videos/{video_filename}"

        if not os.path.exists(video_path):
            video_filename = "default.mp4"  # fallback if video doesn't exist
            video_path = f"static/videos/{video_filename}"

        video_url = f"/static/videos/{video_filename}"
        return jsonify({'hindi': hindi_text, 'video_url': video_url})

    except Exception as e:
        print(f"Translation Error: {e}")
        return jsonify({'error': 'Translation failed'})

@app.route('/verify')
def verify_gesture():
    word = request.args.get('word', '')
    match = random.choice([True, False])
    return jsonify({'match': match})

if __name__ == '__main__':
    app.run(debug=True)
    
