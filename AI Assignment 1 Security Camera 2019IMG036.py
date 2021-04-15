import cv2

import time

from datetime import datetime

from sinchsms import SinchSMS

import pyttsx3


# function for sending SMS
def sendSMS():A
    number = 'your_mobile_number'
    app_key = 'your_app_key'
    app_secret = 'your_app_secret'

    # enter the message to be sent
    message = 'Motion Detected in your Security cam at' + datetime.now()

    client = SinchSMS(app_key, app_secret)
    print("Sending '%s' to %s" % (message, number))

    response = client.send_message(number, message)
    message_id = response['messageId']
    response = client.check_status(message_id)

    # keep trying unless the status retured is Successful
    while response['status'] != 'Successful':
        print(response['status'])
        time.sleep(1)
        response = client.check_status(message_id)

    print(response['status'])


faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
bodyCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cam = cv2.VideoCapture(1)
if cam.isOpened():
  print ("Connected....")
  while True:
     # Capture frame-by-frame
     ret, frame = cam.read()
     if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )
        body = bodyCascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in body:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            if(body.any()):
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[1].id)
                engine.setProperty('rate', 150)
                engine.say("Object Detected")
                engine.runAndWait()
                try:
                    sendSMS()
                except:
                    print("failed to communicate")
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

     else:
        print ("Error aqcuiring the frame")
        break

     if cv2.waitKey(1) & 0xFF == ord('q'):
        break
else:
   print("not connected")

# When everything is done, release the capture
cam.release()
cv2.destroyAllWindows()