# Filecannon

You may know the feeling of needing to move files between phone and computer quickly and without losing data (e.g. image quality). One approach is to ZIP it and upload to a file sharing service.

This is the faster and easier alternative with a web interface, hosted entirely on your machine (speed and privacy go brr)


## How It Works
1. Launch the Flask server
2. Access the web server from another LAN device `http://<HOST-IP>:<APP-PORT>`
3. Upload and download files as you wish
4. Hit the `Clear` button when the database becomes too large

Secure from other users on the same network? **Nope!** ...but convenient.

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

    gunicorn -c gunicorn.conf.py wsgi:app

### Access the web server from other devices
If host machine has IP `192.168.0.50`, and the app runs on port `8080`, then another device on the LAN can go to `http://192.168.0.50:8080` to access.

---

## Screenshot

![Screenshot from 2023-04-17 18-24-23](https://user-images.githubusercontent.com/120788835/232559023-be7217af-71ad-441a-994f-12fc0781590b.png)