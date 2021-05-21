from flask  import Flask, render_template, send_from_directory, send_file, Response, request
import numpy as np
import cv2
import pathlib
from flask.helpers import make_response
import io
import imutils
from PIL import Image


myapp = Flask(__name__, static_url_path="", static_folder="static")

def analyseImagebyColor(lower_mask, upper_mask, image, color_name, color_contour):
    imageConverted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imageConverted = cv2.GaussianBlur(imageConverted, (5, 5), 0)
    
    mask = cv2.inRange(imageConverted, lower_mask, upper_mask)

    print("Buscando Contornos")
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)

    print("Desenhando Contornos")
    cnts_imutils = imutils.grab_contours(cnts)
    for c in cnts_imutils:
        cv2.drawContours(image, [c], -1, color_contour, 2)
    
    return image

@myapp.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux";

@myapp.route("/analyser")
def analyserTestImage():
    imageOriginal = cv2.imread("static\\two_pencil.jpg")

    lower_blue = np.array([75, 151, 121], dtype="uint8") #Azul
    upper_blue = np.array([127, 236, 255], dtype="uint8") #Azul
    imageOriginal = analyseImagebyColor(lower_blue, upper_blue, imageOriginal, "Azul",(0,255,0))
    
    lower_yellow = np.array([25, 50, 40], dtype="uint8") #Amarelo
    upper_yellow = np.array([35, 255, 255], dtype="uint8") #Amarelo
    imageOriginal = analyseImagebyColor(lower_yellow, upper_yellow, imageOriginal, "Amarelo", (255,0,0))
    
    print("Codificando Imagem")    
    data = cv2.imencode('.png', imageOriginal)[1].tobytes()
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')


@myapp.errorhandler(Exception)
def exception_handler(error):
    return repr(error), 500