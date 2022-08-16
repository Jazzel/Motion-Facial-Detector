from gpiozero import MotionSensor,Buzzer,DistanceSensor
import smtplib
import ssl
import picamera
from datetime import datetime
from email.message import EmailMessage
from time import sleep
import glob
import cv2 as cv
from PIL import Image
import face_recognition
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials
import os


import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyAcI-bAEejoAutwUdfPUszwKcQv-Irw1eM",
    'authDomain': "home-faf58.firebaseapp.com",
    'projectId': "home-faf58",
    'storageBucket': "home-faf58.appspot.com",
    'messagingSenderId': "741737162371",
    'appId': "1:741737162371:web:43a8a2e645122c580d1db6",
    'measurementId': "G-DCJGXH5F3B", 
    'databaseURL': "https://home-faf58-default-rtdb.firebaseio.com/"
}
firebase = pyrebase.initialize_app(firebaseConfig)
cred = credentials.Certificate("/home/pi/Desktop/absolute-point-359510-b4e8869404b5.json")
firebase_admin.initialize_app(cred)

storage = firebase.storage()

motion_sesnor = MotionSensor(26)
buzzer = Buzzer(2)
sensor = DistanceSensor(echo=21, trigger=14, max_distance=2.0)
email_sender = 'codetitans678@gmail.com'
email_password = 'hcfvuvxtlbigzhqb'
email_receiver = 'titans_code21@yahoo.com'

subject = 'ALERT!'
body = """
Some one Entered
""" + str(sensor.distance * 100)

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()
camera = picamera.PiCamera()
moiz = face_recognition.load_image_file("/home/pi/Desktop/moiz.jpg")
moiz_encod = face_recognition.face_encodings(moiz)

while True:
    motion_sesnor.wait_for_motion()
    print("MOTION DETECTED");
    buzzer.on()
    distance = sensor.distance * 100
    print("Distance : %.1f" % distance)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    print("Email Sent")
    camera.start_preview()
    sleep(1)
    camera.capture('/home/pi/img/predictions/unkown/'+str(datetime.now())+'.jpg')
    camera.stop_preview()
    print("pushed")
    now = datetime.now()
    dt = now.strftime("%d%m%Y%H:%M:%S")
    name = dt+".jpg"
    camera.capture(name)
    print(name+" saved")
    storage.child(name).put(name)
    print("Image sent")
    os.remove(name)
    print("File Removed")
    sleep(1)
    motion_sesnor.wait_for_no_motion()
    print("MOTION not DETECTED");
    buzzer.off()
    sleep(1)
    
image = []
path = glob.glob("/home/pi/img/predictions/unkown/*.jpg")
cv_img = []
for img in path:
    n = cv.imread(img)
    cv_img.append(n)
    image.append(img)
print(image[0])    
img = cv.imread(image[0], cv.IMREAD_COLOR)

cv.imshow("image", img)

cv.waitKey(0)
cv.destroyAllWindows()
pre = face_recognition.load_image_file(image[0])
preenc = face_recognition.face_encodings(pre)
matches = face_recognition.compare_faces(moiz_encod,preenc)
print(matches)