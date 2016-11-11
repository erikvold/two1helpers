# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 13:25:09 2016


@author: fred
"""
import configparser
import json
from flask import request
import shlex
import subprocess

def json2shell():
    """this function runs a shell command with options and returns stdout"""

    config = configparser.ConfigParser()
    config.read("config.ini")
    mycwd = config.get("Paths", "mycwd")
    pathtobin = config.get("Paths", "pathtobin")
    print('pathtobin is ' + pathtobin)

    flags = json.loads(request.data.decode('UTF-8'))
    optvalue = shlex.quote(flags['options'])
    print('options received are ' + flags['options'])
    print('command line will be ' + pathtobin + ' ' + optvalue)
    commandline = pathtobin + ' ' + optvalue

    args = shlex.split(commandline)
    print(args)
    output = subprocess.check_output(args, cwd = mycwd)

    return output

