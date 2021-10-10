from flask import Flask, render_template, request, make_response
import pyqrcode
import hashlib
from flask import session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "328489f5a3ddecc38ecad56b97441a48d9c9a186"


def generate_qrcode(text):
    qr = pyqrcode.QRCode(text)
    filename = session['filename']
    if not os.path.exists('static/temp'):
        os.mkdir('static/temp')
    qr.png(f'./static/temp/{filename}', scale=8)

def set_filename(text):
    hash = hashlib.md5(text.encode()).hexdigest()
    session['filename'] = f"qrcode_{hash}.png"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['qrcode-text']        
        set_filename(text)
        generate_qrcode(text)
    results ={}
    try:
        filename=session["filename"]
        if os.path.exists(f"static/temp/{filename}"):
            results = {"filename": "temp/" + session["filename"]}
        else:
            results['filename'] = False
    except KeyError:
        results['filename'] = False

    return render_template('index.html', results = results)

@app.route('/download')
def download():
    filename = session['filename']
    path = f'static/temp/{filename}'
    def generate():
        with open(path, 'rb') as f:
            data = f.read()
        os.remove(path)
        return data
    response = make_response(generate())
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition', 'attachment', filename="qrcode.png")
    return response

if __name__ =="__main__":
    app.run(debug=True)