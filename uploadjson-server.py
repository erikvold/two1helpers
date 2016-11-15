# -*- coding: utf-8 -*-
"""
Server stub that uploads json file from local computer, converts
to a dictionary, and returns result of function performed

Created on November 15, 2016

@author: Fred Zimmerman
"""
import subprocess
import os
import psutil
import json
import configparser

from flask import Flask, request
from werkzeug.utils import secure_filename

import logging
from logging import FileHandler

# import two1 libraries

from two1.wallet import Wallet
from two1.bitserv.flask import Payment

# Configure the app and wallet
app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

file_handler = FileHandler("/tmp/debug.log","a")
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['json'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/buy', methods=['GET', 'POST'])
@payment.required(10000)

def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = str((os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            with open(filename) as json_data:
                d = json.load(json_data)
                # act on d
                # define variable to return
                success = 'Successfully uploaded file' + ' ' + filename
                success = success + ' ' + 'and performed function'
                return success

# Initialize and run the server
if __name__ == '__main__':

   import click

   @click.command()
   @click.option("-d", "--daemon", default=False, is_flag=True,
                  help="Run in daemon mode.")

   def run(daemon):
            if daemon:
                pid_file = './uploadjson.pid'
                if os.path.isfile(pid_file):
                    pid = int(open(pid_file).read())
                    os.remove(pid_file)
                    try:
                        p = psutil.Process(pid)
                        p.terminate()
                    except:
                        pass
                try:
                    p = subprocess.Popen(['python3', 'uploadjson-server.py'])
                    open(pid_file, 'w').write(str(p.pid))
                except subprocess.CalledProcessError:
                    raise ValueError("error starting uploadjson-server.py daemon")
            else:
                print("uploadjson-server.py running...")
                app.run(host='::', port=5034, debug=True)
   run()
