# Filecannon

You may know the feeling of needing to move files between phone and computer quickly and without losing data (e.g. image quality). One approach is to ZIP it and upload to a file sharing service.

This is the faster and easier alternative with a web interface, hosted entirely on your machine (speed and privacy go brr)


## How It Works
1. Launch the Flask server
2. Access the web server from another LAN device
3. Upload and download files as you wish

---

## Preparation
### [Optional] Setup venv
1.1 Create venv

    python -m venv venv

1.2 Activate the venv

    Linux: source venv/bin/activate
    Windows: venv\Scripts\Activate

### 1) Install requirements.txt
    pip install -r requirements.txt

### 2) Run the setup
    python setup.py

---

## Run it!
Launch the app by running:

    gunicorn -c conf.py  "wsgi:start()" 

---

## Screenshot

![image](https://github.com/cleanmountain/filecannon/assets/120788835/3f23b28d-3ea6-4a80-8c8e-28e1998a9662)
