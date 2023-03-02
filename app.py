import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, Response
from werkzeug.utils import secure_filename
from config import Config
from projects.object_detection import obj_detect_model
from projects.face_expression import expression_model
from hub import allow_file
import numpy as np



app = Flask(__name__)

# all the pages
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("index.html")

@app.route('/services#<section_id>')
def services(section_id):
    return render_template('index.html', section_id=section_id)


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/contact")
def contact():
    return render_template("index.html")


# object_detect

@app.route('/image_detect')
def image_detect():
    return render_template('image_detect.html')



# stock price

@app.route('/stock_prediction')
def stock_prediction():
    return render_template('stock_prediction.html')


# face recognition

@app.route('/face_recognize')
def face_recognize():
    return render_template('face_express_recognize.html')


# emotion analysis
@app.route('/emotion_analysis')
def emotion_analysis():
    return render_template('emotion_analysis.html')


# xray
@app.route('/detecting_pneumonia')
def detecting_pneumonia():
    return render_template('chest_xray.html')


# car prices
@app.route('/price_prediction')
def price_prediction():
    return render_template('car_price_predition.html')


if __name__ == "__main__":
    app.run(debug=True)