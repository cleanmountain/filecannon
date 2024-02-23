import os
import uuid
import datetime
from pathlib import Path
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
app.secret_key = "donkey"
app.config["UPLOAD_FOLDER"] = "static/files"

db = SQLAlchemy(app)

class Upload(db.Model):
    id = db.Column(db.String, primary_key=True)
    filename = db.Column(db.String)
    timestamp = db.Column(db.String)
    timestamp_formatted = db.Column(db.String)
    path = db.Column(db.String)
    size_bytes = db.Column(db.BigInteger)
    size_formatted = db.Column(db.String)

@app.route("/", methods=["GET", "POST"])
def uploads_overview():
    uploads = Upload.query.order_by(Upload.timestamp.desc()).all()
    return render_template("uploads.html", uploads=uploads)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    upload_count = 0

    if request.method == "POST":
        files = request.files.getlist("file")
        
        if not files[0].filename:
            flash("No file was submitted.", "error")
            return redirect(url_for("upload"))            

        for file in files:
            upload_count += 1
            upload_id = str(uuid.uuid4())
            Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], upload_id))
            path = f"{app.config['UPLOAD_FOLDER']}/{upload_id}"
            file_size = os.stat(path).st_size
            upload = Upload(id=upload_id, filename=file.filename, timestamp=get_time(), timestamp_formatted=get_time(format=True), path=path, size_bytes=file_size, size_formatted=format_file_size(file_size))
            db.session.add(upload)
            db.session.commit()
        
        flash(f"Uploaded {upload_count} file(s)!", "success")
        upload_count = 0
        return redirect(url_for("upload"))

    return render_template("upload-file.html")


@app.route("/download/<upload_id>")
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(upload.path, download_name=upload.filename, as_attachment=True)


@app.route("/clear")
def clear():
    uploads = Upload.query.order_by(Upload.id.desc()).all()
    
    for upload in uploads:
        os.remove(os.path.join(upload.path))

    Upload.query.delete()
    db.session.commit()
    return redirect(url_for("uploads_overview"))


@app.route("/access")
def access():
    return render_template("access.html")


def get_time(format=False) -> str:
    time = datetime.datetime.now()
    if format:
     return time.strftime("%Y-%m-%d %H:%M:%S")
    return time


def format_file_size(b):
    kb = b / 1024
    mb = kb / 1024
    gb = mb / 1024

    if gb >= 1:
        return f"{gb:.2f} GB"
    if mb >= 1:
        return f"{mb:.2f} MB"
    if kb >= 1:
        return f"{kb:.2f} KB"
    
    return f"{b} B"
