import os
from uuid import uuid4

from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.exceptions import (HTTPException, InternalServerError,
                                 RequestEntityTooLarge)
from werkzeug.utils import secure_filename

from extract import process

# File extensions that are acceptable to upload
ALLOWED_EXTENSIONS = {"jpg", "jpeg"}

# Designated a folder for user's upload
UPLOAD_FOLDER = "static/clients_upload"

app = Flask(__name__)

# Configuration for upload folder
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Configuartion for Secret Key and file size limit
app.config.from_pyfile("config.cfg")
if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY is not set")


# Delete the previous files and clear the session
def cleanup():
    if os.path.exists(session["filepath"]):
        os.remove(session["filepath"])
        os.rmdir(session["folder"])
        session.clear()


# Check if file extnesion is allowed
def allowed_ext(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["id"] = session.get("id")
        try:
            file = request.files["file"]
        
        # validate file
        except RequestEntityTooLarge:
            flash("File exceed size limit.")
            return redirect(request.url)
        if file.filename == "":
            flash("No file selected.")
            return redirect(request.url)
        elif not allowed_ext(file.filename):
            flash("Not supported file.")
            return redirect(request.url)
        session["filename"] = secure_filename(file.filename)
        session["folder"] = os.path.join(
            app.config["UPLOAD_FOLDER"], str(session["id"]))
        
        # create directory and store upload image
        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        if not os.path.exists(session["folder"]):
            os.mkdir(session["folder"])
        session["filepath"] = os.path.join(
            session["folder"], session["filename"])
        file.save(session["filepath"])

        # extract exif data from file
        data = process(file)
        return render_template("result.html", session=session, data=data)
    else:
        
        # If pic already exist in the session then reset
        if session.get("filepath"):
            cleanup()
        
        # Assign a new seesion
        if session.get("id") is None:
            session["id"] = uuid4()
        return render_template("index.html")


# handel errors
@app.errorhandler(Exception)
def handle_error(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)


# custom error page
def error(message, code=400):
    return render_template("error.html", code=code, message=message), code
