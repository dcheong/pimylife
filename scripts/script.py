import os
import sys
import datetime
import keyboard
import io
import picamera

baseVidDir = "/home/pi/SAUCGTC/videos/"
initTime = datetime.datetime.now()
vidDir = baseVidDir + initTime.date().__str__() + "/"

# Video segments are 30s long
videoLength = 30

# Make directory if it doesn't exist
if not os.path.exists(vidDir):
  os.makedirs(vidDir)

stream = io.BytesIO()
camera = picamera.PiCamera()

camera.start_preview(fullscreen=False, window = (100, 20, 640, 480))
camera.resolution = (640,480)
camera.start_recording(vidDir + initTime.time().__str__() + ".h264")

while True:
  if keyboard.is_pressed('q'):
    camera.stop_recording()
    camera.stop_preview()
    camera.close()
    print 'Quitting'
    break
  timeNow = datetime.datetime.now()
  if timeNow.date().__str__() != initTime.date().__str__():
    if not os.path.exists(vidDir):
      os.makedirs(vidDir)
    vidDir = baseVidDir + timeNow.date().__str__() + "/"
  # Check if it is time to begin a new video segment
  if (timeNow - initTime).total_seconds() >= videoLength:
    print 'Starting new recording at ' + vidDir
    camera.stop_recording()
    initTime = timeNow
    camera.start_recording(vidDir + initTime.time().__str__() + ".h264")
