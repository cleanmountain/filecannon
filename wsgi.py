import qrcode
from conf import bind
from app import app

def start():
    make_shortcut_qr(f"http://{bind}")
    _green = '\033[92m'
    _nc = '\033[0m'
    print(_green + f"FILECANNON IS NOW ACCESSIBLE AT http://{bind}" + _nc)
    print(_green + f"FILECANNON IS NOW ACCESSIBLE AT http://{bind}" + _nc)
    return app

def make_shortcut_qr(url) -> None:
    qr = qrcode.QRCode(border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#c2ff7b", back_color="#303036")
    img.save("./static/qr.png")

if __name__ == "__main__":
    app.run()
