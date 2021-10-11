from flask import Flask, render_template, request, make_response, session
import pyqrcode
import hashlib
import os
from PIL import ImageColor

filenames = []

app = Flask(__name__)
app.config["SECRET_KEY"] = "328489f5a3ddecc38ecad56b97441a48d9c9a186"


def generate_qrcode(text):
    qr = pyqrcode.QRCode(text)
    filename = session["filename"]
    if not os.path.exists("static/temp"):
        os.mkdir("static/temp")
    if session["filetype"] == 1:
        qr.png(
            f"./static/temp/{filename}",
            scale=8,
            background=ImageColor.getcolor(session["background_hex"], "RGB"),
            module_color=ImageColor.getcolor(session["foreground_hex"], "RGB"),
        )
    elif session["filetype"] == 2:
        qr.svg(
            f"./static/temp/{filename}",
            scale=8,
            background=session["background_hex"],
            module_color=session["foreground_hex"],
        )


def set_filename(text):
    text = (
        text
        + session["background_hex"]
        + session["foreground_hex"]
        + str(session["filetype"])
    )
    hash = hashlib.md5(text.encode()).hexdigest()
    if session["filetype"] == 1:
        session["filename"] = f"qrcode_{hash}.png"
    elif session["filetype"] == 2:
        session["filename"] = f"qrcode_{hash}.svg"
    filenames.append(session["filename"])


def remove_extra_files():
    if len(filenames) > 20:
        for files in filenames[0:10]:
            filenames.pop(filenames.index(files))
            os.remove(f"./static/temp/{files}")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["qrcode-text"]
        session["background_hex"] = request.form.get("background", "")
        session["foreground_hex"] = request.form.get("foreground", "")
        session["filetype"] = int(request.form["filetype"])
        set_filename(text)
        generate_qrcode(text)
        remove_extra_files()
    results = {}
    try:
        filename = session["filename"]
        if os.path.exists(f"static/temp/{filename}"):
            results = {"filename": "temp/" + session["filename"]}
        else:
            results["filename"] = False
    except KeyError:
        results["filename"] = False

    return render_template("index.html", results=results)


@app.route("/download")
def download():
    filename = session["filename"]
    path = f"static/temp/{filename}"

    def generate():
        with open(path, "rb") as f:
            data = f.read()
        os.remove(path)
        return data

    response = make_response(generate())
    if session["filetype"] == 1:
        response.headers.set("Content-Type", "image/png")
        response.headers.set("Content-Disposition", "attachment", filename="qrcode.png")
    elif session["filetype"] == 2:
        response.headers.set("Content-Type", "image/svg+xml")
        response.headers.set("Content-Disposition", "attachment", filename="qrcode.svg")
    return response


if __name__ == "__main__":
    app.run(debug=True)
