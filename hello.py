from flask  import Flask, render_template, send_from_directory, send_file, Response, request
import numpy as np
import cv2
import pathlib
from flask.helpers import make_response
import io
import requests
import imutils
import base64
import uuid

myapp = Flask(__name__)

def analyseImagebyColor(lower_mask, upper_mask, image):
    imageConverted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imageConverted = cv2.GaussianBlur(imageConverted, (5, 5), 0)
    
    mask = cv2.inRange(imageConverted, lower_mask, upper_mask)

    print("Buscando Contornos...")
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    
    return cnts

def drawContour(cnts,image,color_contour,color_name):
    print("Desenhando Contornos...")
    cnts_imutils = imutils.grab_contours(cnts)
    for c in cnts_imutils:
        try: 
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.putText(image, color_name, (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        except:
            print("Erro ao centralizar nome")
        
        cv2.drawContours(image, [c], -1, color_contour, 2)
        
    return image

def uploadToS3(image,token):
    headers = {'x-access-token' : token}
    data = {"fileType": ".png"}
    r = requests.post("https://helptonic-api.azurewebsites.net/s3",data=data,headers=headers)
    if r.ok:
        response = r.json()
        if response['success']:
            print("Enviando para o S3...")    
            responseUplodad = requests.put(response['uploadUrl'], data=image)
            if responseUplodad.ok:
                print("Enviado com sucesso..")  
                return True, response['downloadUrl']
            else:
                return False, 'Erro enviar dados ao servidor S3.'
        else:
            return False, response['message']
    else:
        return False, 'Erro enviar dados ao servidor de dados.'
    
    print(r)

@myapp.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux";

@myapp.route("/analyser", methods=['POST'])
def analyserTestImage():
    base64Image = request.json['image']
    tokenUser = request.json['token']
    
    image_bytes = base64.b64decode(base64Image)
    im_arr = np.frombuffer(image_bytes, dtype=np.uint8)
    imageOriginal = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    
    lower_orange = np.array([5, 38, 40], dtype="uint8") #Laranja
    upper_orange = np.array([15, 255, 255], dtype="uint8") #Laranja
    cnts_orange = analyseImagebyColor(lower_orange, upper_orange, imageOriginal)
    
    lower_yellow = np.array([20, 50, 40], dtype="uint8") #Amarelo
    upper_yellow = np.array([35, 255, 255], dtype="uint8") #Amarelo
    cnts_yellow = analyseImagebyColor(lower_yellow, upper_yellow, imageOriginal)
    
    lower_green = np.array([45, 38, 40], dtype="uint8") #Verde
    upper_green = np.array([80, 255, 255], dtype="uint8") #verde
    cnts_green = analyseImagebyColor(lower_green, upper_green, imageOriginal)
    
    lower_blue = np.array([81, 38, 40], dtype="uint8") #Azul
    upper_blue = np.array([127, 255, 255], dtype="uint8") #Azul
    cnts_blue = analyseImagebyColor(lower_blue, upper_blue, imageOriginal)
    
    lower_purple = np.array([130, 38, 40], dtype="uint8") #Roxo
    upper_purple = np.array([144, 255, 255], dtype="uint8") #Roxo
    cnts_purple = analyseImagebyColor(lower_purple, upper_purple, imageOriginal)
    
    lower_pink = np.array([145, 38, 40], dtype="uint8") #Rosa
    upper_pink = np.array([160, 255, 255], dtype="uint8") #Rosa
    cnts_pink = analyseImagebyColor(lower_pink, upper_pink, imageOriginal)
    
    imageOriginal = drawContour(cnts_orange,imageOriginal,(255,0,0),"Laranja")
    imageOriginal = drawContour(cnts_yellow,imageOriginal,(0,255,0), "Amarelo") 
    imageOriginal = drawContour(cnts_green,imageOriginal,(0,0,255), "Verde")
    imageOriginal = drawContour(cnts_blue,imageOriginal,(0,255,255),  "Azul")
    imageOriginal = drawContour(cnts_purple,imageOriginal,(255,255,0), "Roxo") 
    imageOriginal = drawContour(cnts_pink,imageOriginal,(255,0,255), "Rosa")
    
    
    print("Codificando Imagem...")    
    data = cv2.imencode('.png', imageOriginal)[1].tobytes()
    print("Buscando url do S3...")    
    success, returnString = uploadToS3(data,tokenUser)
    print(returnString)  
    if success:
        return returnString
    else:
        return returnString, 500



@myapp.errorhandler(Exception)
def exception_handler(error):
    return repr(error), 500
