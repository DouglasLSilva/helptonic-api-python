from flask  import Flask, render_template, send_from_directory
import pathlib

myapp = Flask(__name__, static_url_path="", static_folder="static")

@myapp.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux";

@myapp.route("/analyser")
def analyserImage():
    return send_from_directory("static","colors.png");

@myapp.errorhandler(Exception)
def exception_handler(error):
    return "!!!!"  + repr(error)