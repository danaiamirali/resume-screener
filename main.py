from flask import Flask, redirect, url_for, render_template, request, session
from flask_socketio import SocketIO
from fitz.utils import getColor
import fitz
import os


app = Flask(__name__, static_folder="static")
app.secret_key = 'resume_screener'
socketio = SocketIO(app, async_mode = 'eventlet')

filename = ""
str = ""

from modules.screener import Screener

#list, each index list of pairs, first index string to highlight, second is color
#feed in colors as string names
def highlight(hi_list):
    global filename
    file = filename[3:]
    doc = fitz.open(file)
    page = doc[0]
    for pair in hi_list:
        text_instances = page.search_for(pair[0])
        color = getColor(pair[1])
        highlight = page.add_highlight_annot(text_instances)
        highlight.set_colors(stroke=color)
        highlight.update()

    #text_instances = page.search_for("Tiernan")      
    #page.add_highlight_annot(text_instances)
    
    file1 = file[:-4]
    file1 = file1 + '1.pdf'
    filename = "../" + file1
    doc.save(file1)
    doc.close()
    file = file1
    socketio.emit('event', namespace='/upload')

@socketio.on('connect', namespace='/upload')
def handle_connect():
    hi_list = []
    highlight(hi_list)
    socketio.emit('redirect', namespace='/upload')
    # do something

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if 'resume' not in request.files or request.files['resume'].filename == '':
            return render_template("home.html")
        else:
            global filename
            job = request.form['job']
            resume = request.files['resume']
            filename = "../static/" + resume.filename
            resume.save('static/' + resume.filename)
            return redirect(url_for("upload"))
    else:
        return render_template("home.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    return render_template("upload.html")

@app.route("/results", methods=["POST", "GET"])
def results():
    return render_template("result.html", path=filename)

if __name__ == "__main__":
    socketio.run(app, debug=True)