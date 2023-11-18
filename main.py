from flask import Flask, redirect, url_for, render_template, request, session
from flask_socketio import SocketIO
import fitz
import os

app = Flask(__name__, static_folder="static")
app.secret_key = 'resume_screener'
socketio = SocketIO(app, async_mode = 'eventlet')

filename = ""
str = ""

from modules.screener import Screener

def highlight():
    global filename
    directory = os.getcwd()
    filename = os.path.join(directory, "uploads", filename)
    doc = fitz.open("uploads/Tiernan_Jesrani_Resume.pdf")
    page = doc[0]
    for rect in page.search_for("Tiernan"):
        page.add_highlight_annot(rect)
    doc.close()
    socketio.emit('event', namespace='/upload')

@socketio.on('connect', namespace='/upload')
def handle_connect():
    #highlight()
    global str
    job_desc = """
    Below are the skills needed for this project. Students with the following relevant skills and interest, regardless of major, are encouraged to apply! This is a team based multidisciplinary project. Students on the team are not expected to have experience in all areas, but should be willing to learn and will be asked to perform a breadth of tasks throughout the two semester project.
    Advanced Data Science and Modeling Techniques
    Specific Skills: Applied project experience with Large Language Models and other applied AI techniques OR advanced coursework

    Likely Majors: DATA, STATS, MATH, CS


    Data Science
    Specific Skills: General skills in Data Science, good software development skills, and a willingness to quickly develop new technical skills as required for the project

    EECS 281(or equivalent) is required

    Likely Majors: DATA, CS


    General Coding
    Specific Skills: General Programming skills, good software engineering practice and design, and a willingness to quickly develop new technical skills as required for the project 

    EECS 281 (or equivalent) is required

    Likely Majors: CS, DATA, BBA/CS



    Additional Desired Skills/Knowledge/Experience
    Successful team-based project experience.  Excellent interpersonal skills
    Project Management utilizing Agile/Scrum
    Experience in business process analysis
    Interest in and general knowledge of Commercial Banking
    Practical experience implementing predictive analytics in a complex data environment
    Ability and desire to independently learn new technology skills as necessary for the project
    Experience implementing large language models, neural networks and self-supervised / semi-supervised learning models
    """
    s = Screener("static/resume.pdf", job_desc)
    str = s.is_correct_fit()
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
            filename = resume.filename
            resume.save('uploads/' + resume.filename)
            return redirect(url_for("upload"))
    else:
        return render_template("home.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    return render_template("upload.html")

@app.route("/results", methods=["POST", "GET"])
def results():
    global str
    return render_template("result.html", str=str)
    



if __name__ == "__main__":
    socketio.run(app, debug=True)