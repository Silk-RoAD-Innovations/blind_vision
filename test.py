from flask import Flask, render_template, request, send_file
import os
import base64
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture_photo', methods=['POST'])
def capture_photo():
    # Retrieve the base64-encoded photo data from the request
    photo_data_url = request.form.get('photo')

    # Decode the base64 data and save it as an image file
    img_data = base64.b64decode(photo_data_url.split(',')[1])
    img_path = 'static/photo.jpg'
    with open(img_path, 'wb') as img_file:
        img_file.write(img_data)

    # Simulate processing time
    time.sleep(2)

    # Return the path to the captured photo
    return img_path

@app.route('/play_audio')
def play_audio():
    # Provide the path to your audio file (sound.mp3)
    audio_path = 'static/sound.mp3'
    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
