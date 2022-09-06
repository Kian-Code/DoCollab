import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC3d37fdd743cf092ec180d7e50ae4f0ad'
    TWILIO_SYNC_SERVICE_SID = 'IS540a8a050255f188b8c1674428293255'
    TWILIO_API_KEY = 'SK55a7c5c2da6505e86b58bee89e9f0e4c'
    TWILIO_API_SECRET = 'jAnXFfZFlmQgqu5RD0ouJoJByZsGwqTH'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    notepad = request.form['text']
    with open('textarea.txt' , 'w') as f:
        f.write(notepad)
    path = "textarea.txt"
    return send_file(path , as_attachment = True)
    
if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
