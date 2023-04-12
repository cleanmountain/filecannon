from io import BytesIO
import datetime
from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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


@app.route("/", methods=["GET", "POST"])
def uploads_overview():
    uploads = Upload.query.order_by(Upload.id.desc()).all()    
    return render_template("uploads.html", uploads=uploads)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
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


def get_time() -> str:
    time: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return time


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)