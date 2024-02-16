import os
import uuid
import datetime
from pathlib import Path
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import qrcode
from get_ip import get_local_ip

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
app.secret_key = "donkey"
app.config["UPLOAD_FOLDER"] = "static/files"

db = SQLAlchemy(app)

class Upload(db.Model):
    id = db.Column(db.String, primary_key=True)
    filename = db.Column(db.String(50))
    timestamp = db.Column(db.String(20))
    path = db.Column(db.String(255))


@app.before_first_request
def my_func():
    host = get_local_ip()
    url = f"http://{host}/"
    make_shortcut_qr(url)


@app.route("/", methods=["GET", "POST"])
def uploads_overview():
    uploads = Upload.query.order_by(Upload.id.desc()).all()    
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
            upload = Upload(id=upload_id, filename=file.filename, timestamp=get_time(), path=path)
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


def get_time() -> str:
    time: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return time


def make_shortcut_qr(url) -> None:
    qr = qrcode.QRCode(border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#FC5130", back_color="#303036")
    img.save("./static/qr.png")
