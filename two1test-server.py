# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:04:52 2016

@author: fred
"""

import os
from flask import Flask
import psutil
import subprocess

from two1.wallet import Wallet
from two1.bitserv.flask import Payment

import two1data

# Configure the app and wallet
app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

@app.route('/test', methods=['GET', 'POST'])
@payment.required(3000)

def test():
   test_return = two1data.json2shell()
   return test_return

# Initialize and run the server
if __name__ == '__main__':

   import click

   @click.command()
   @click.option("-d", "--daemon", default=False, is_flag=True,
                  help="Run in daemon mode.")

   def run(daemon):
            if daemon:
                pid_file = './two1test-server.pid'
                if os.path.isfile(pid_file):
                    pid = int(open(pid_file).read())
                    os.remove(pid_file)
                    try:
                        p = psutil.Process(pid)
                        p.terminate()
                    except:
                        pass
                try:
                    p = subprocess.Popen(['python3', 'two1test-server.py'])
                    open(pid_file, 'w').write(str(p.pid))
                except subprocess.CalledProcessError:
                    raise ValueError("error starting two1test-server.py daemon")
            else:
                print("two1test server running...")
                app.run(host='::', port=9999, debug=True)
   run()
