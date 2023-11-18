from flask import Flask, redirect, url_for, render_template, request, session
from flask_socketio import SocketIO


app = Flask(__name__, static_folder="static")
app.secret_key = 'resume_screener'
socketio = SocketIO(app, async_mode = 'eventlet')


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        resume = request.files['resume']
        resume.save('uploads/' + resume.filename)
        return redirect(url_for("upload"))
    else:
        return render_template("home.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    
    return render_template("upload.html")
    



if __name__ == "__main__":
    socketio.run(app, debug=True)