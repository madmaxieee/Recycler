# from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
import picam_fps
import time
from time import sleep
from picamera import PiCamera
import smbus
interpreter = tflite.Interpreter(model_path="/home/pi/Documents/waste20220311_nasnet.tflite")
interpreter.allocate_tensors()
classes=['can','paperbox','PET']
camera=PiCamera()
rpi = smbus.SMBus(1)

arduino = 0x04

result=[]
cap=cv2.VideoCapture(0)

def writeData(value):
    rpi.write_byte(arduino, value)
    return -1

def readData():
    number = rpi.read_byte(arduino)
    return number
 
while(True):
    if readData()=='w':
        sleep(2.0)
        ret, img = cap.read()
        img=cv2.resize(img,(224,224))
        img_tensor=image.img_to_array(img)
        img_tensor=img_tensor/255.
        img_tensor=np.expand_dims(img_tensor,axis=0)
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        interpreter.set_tensor(input_details[0]['index'], img_tensor)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        output=classes[np.argmax(output_data)]
        print(output)
        if output=='paperbox':
            result.append('p')
        elif output=='can':
            result.append('c')
        elif output=='PET':
            result.append('b')
    if readData()=='s':
        for r in result:
            writeData(r)
        result.clear()
