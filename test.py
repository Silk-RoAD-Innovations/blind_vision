from flask import Flask, render_template, request, send_file
import os
import base64
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host="0.0.0.0")
