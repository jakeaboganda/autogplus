#!/usr/bin/env python2.7

import cv2
import numpy
import os
import imutils
import argparse
import time
import ctypes
import math
import subprocess
import sys

ADB = '/Users/jake/Library/Android/sdk/platform-tools/adb'
SCREENCAP_LOC = './screen.png'
DISPLAY_IMAGE = False

def toggleConnect():
    os.popen(ADB + ' shell input tap 780 190').read()

def runScript():
    os.popen(ADB + ' shell input tap 819 1580').read()

def is_connected():
    pipe = subprocess.Popen(ADB + " shell screencap -p",
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, shell=True)
    image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
    image = cv2.imdecode(numpy.fromstring(image_bytes, numpy.uint8), cv2.IMREAD_COLOR)

    crop_img = image[1500:1600, 800:900] 
    #crop_img = cv2.resize(crop_img, (0,0), fx=0.5, fy=0.5)

    if DISPLAY_IMAGE is True:
        cv2.imshow("", crop_img)

    px = crop_img[50][30]

    if DISPLAY_IMAGE is True:
        cv2.waitKey(1)

    # Detect white
    if px[0] == 255 and px[1] == 255 and px[2] == 255:
        # Script "confirmed" that the beacon is not connected
        return False
    
    # Script "confirmed" that the beacon is connected
    return True

while True:
    counter = 0
    sys.stdout.write("[{0}] Starting test round ".format(counter))
    time.sleep(2)

    while True:
        if not is_connected():
            # Detected that the beacon is not connected
            # Pressing connect
            sys.stdout.write(".")
            toggleConnect()
            time.sleep(8)
        else:
            break

    # Running script
    sys.stdout.write(".")
    runScript()
    time.sleep(2)

    # Trying to disconnect
    sys.stdout.write("<END>\n")
    toggleConnect()



