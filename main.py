from flask import Flask, redirect, url_for, render_template, request, session
from flask_socketio import SocketIO
import fitz

app = Flask(__name__, static_folder="static")
app.secret_key = 'resume_screener'
socketio = SocketIO(app, async_mode = 'eventlet')

def highlight(filename):
    doc = fitz.open('uploads/' + filename)
    page = doc[0]
    for rect in page.search_for("Tiernan"):
        page.add_highlight_annot(rect)
    doc.close()


@socketio.on('connect', namespace='/upload')
def handle_connect():
    highlight("test")
    # do something

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if 'resume' not in request.files or request.files['resume'].filename == '':
            return render_template("home.html")
        else:
            job = request.form['job']
            resume = request.files['resume']
            resume.save('uploads/' + resume.filename)
            return redirect(url_for("upload"))
    else:
        return render_template("home.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    return render_template("upload.html")

@app.route("/results", methods=["POST", "GET"])
def results():
    return render_template("result.html")
    



if __name__ == "__main__":
    socketio.run(app, debug=True)