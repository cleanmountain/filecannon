import os
from io import BytesIO
import datetime
from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import qrcode

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
app.secret_key = "donkey"

db = SQLAlchemy(app)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    timestamp = db.Column(db.String(19))
    data = db.Column(db.LargeBinary)

@app.before_first_request
def my_func():
    host = request.host
    print(f"host is: {host}")
    url = f"http://{host}/"
    make_shortcut_qr(url)


@app.route("/", methods=["GET", "POST"])
def uploads_overview():
    uploads = Upload.query.order_by(Upload.id.desc()).all()    
    return render_template("uploads.html", uploads=uploads)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        files = request.files.getlist("file")
        for file in files:
            upload = Upload(filename=file.filename, data=file.read(), timestamp=get_time())
            db.session.add(upload)
            db.session.commit()
        return redirect(url_for("uploads_overview"))
    
    return render_template("upload-file.html")


@app.route("/download/<upload_id>")
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), download_name=upload.filename, as_attachment=True)


@app.route("/clear")
def clear():
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
    print(f"made image from qr")
    img.save("./static/qr.png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
