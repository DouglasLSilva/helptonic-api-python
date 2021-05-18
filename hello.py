from flask  import Flask, render_template, send_from_directory, send_file, Response
import numpy as np
import cv2
import pathlib
from flask.helpers import make_response
import io
import imutils


myapp = Flask(__name__, static_url_path="", static_folder="static")

@myapp.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux";

@myapp.route("/analyser")
def analyserImage():
    imageOriginal = cv2.imread("static\\two_pencil.png")
    image = cv2.cvtColor(imageOriginal, cv2.COLOR_BGR2HSV)
    image = cv2.GaussianBlur(image, (5, 5), 0)

    #Mascapa por Cor
    lower_blue = np.array([97, 100, 117], dtype="uint8") #Azul
    upper_blue = np.array([117, 255, 255], dtype="uint8") #Azul
    mask = cv2.inRange(image, lower_blue, upper_blue)

    #Buscando os contornos
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)

    #Desenhando os contornos
    cnts_imutils = imutils.grab_contours(cnts)
    for c in cnts_imutils:
        cv2.drawContours(imageOriginal, [c], -1, (0, 255, 0), 3)
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.putText(imageOriginal, "Cor Azul", (cX - 10, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    data = cv2.imencode('.png', imageOriginal)[1].tobytes()
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')

@myapp.errorhandler(Exception)
def exception_handler(error):
    return "!!!!"  + repr(error)