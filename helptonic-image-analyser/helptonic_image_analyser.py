import flask
from flask import send_file

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/analyser', methods=['GET'])
def imageAnalyser():
    filename = 'images\\twittercard.png'
    return send_file(filename, mimetype='image/png')




@app.route('/health-check', methods=['GET'])
def healthcheck():
    status_code = flask.Response(status=200)
    return status_code

app.run()
