from flask  import Flask, render_template, send_from_directory, send_file, Response, request
import numpy as np
import cv2
import pathlib
from flask.helpers import make_response
import io
import imutils
from PIL import Image


myapp = Flask(__name__, static_url_path="", static_folder="static")

def analyseImagebyColor(lower_mask, upper_mask, image, color_name):
    imageConverted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imageConverted = cv2.GaussianBlur(imageConverted, (5, 5), 0)
    
    mask = cv2.inRange(imageConverted, lower_mask, upper_mask)

    print("Buscando Contornos")
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)


    
    return cnts

def drawContour(cnts,image,color_contour):
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
    imageOriginal = cv2.imread("static\\Arcoiris.png")
    
    lower_yellow = np.array([25, 50, 40], dtype="uint8") #Amarelo
    upper_yellow = np.array([35, 255, 255], dtype="uint8") #Amarelo
    cnts_yellow = analyseImagebyColor(lower_yellow, upper_yellow, imageOriginal, "Amarelo")
    
    lower_blue = np.array([75, 151, 121], dtype="uint8") #Azul
    upper_blue = np.array([127, 255, 255], dtype="uint8") #Azul
    cnts_blue = analyseImagebyColor(lower_blue, upper_blue, imageOriginal, "Azul")
    
    lower_green = np.array([40, 38, 40], dtype="uint8") #Verde
    upper_green = np.array([90, 200, 200], dtype="uint8") #verde
    cnts_green = analyseImagebyColor(lower_green, upper_green, imageOriginal, "Verde")
    
    imageOriginal = drawContour(cnts_yellow,imageOriginal,(255,0,0)) #Contorno Amarelo
    imageOriginal = drawContour(cnts_blue,imageOriginal,(0,255,0)) #Contorno Azul
    imageOriginal = drawContour(cnts_green,imageOriginal,(0,0,255)) #Contorno Verde
    
    
    print("Codificando Imagem")    
    data = cv2.imencode('.png', imageOriginal)[1].tobytes()
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')


@myapp.errorhandler(Exception)
def exception_handler(error):
    return repr(error), 500