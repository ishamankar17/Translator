import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template
from googletrans import Translator
import os
import random

app = Flask(__name__)
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate_new')
def translate_word():
    word = request.args.get('word', '').strip()
    try:
        translated = translator.translate(word, src='en', dest='hi')
        hindi_text = translated.text

        # Build video file path
        video_filename = f"{word.capitalize()}.mp4"
        video_path = f"static/videos/{video_filename}"

        if not os.path.exists(video_path):
            video_filename = "default.mp4"
            video_path = f"static/videos/{video_filename}"

        video_url = f"/static/videos/{video_filename}"
        return jsonify({'hindi': hindi_text, 'video_url': video_url})

    except Exception as e:
        print(f"Translation Error: {e}")
        return jsonify({'error': 'Translation failed'})

@app.route('/verify', methods=['POST'])
def verify_gesture():
    try:
        image_file = request.files['image']
        image = np.frombuffer(image_file.read(), np.uint8)
        img = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Process Image (Fake logic for demo)
        match = random.choice([True, False])  # Replace with AI model comparison

        return jsonify({'match': match})
    except Exception as e:
        print(f"Verification Error: {e}")
        return jsonify({'error': 'Gesture verification failed'})

if __name__ == '__main__':
    app.run(debug=True)
