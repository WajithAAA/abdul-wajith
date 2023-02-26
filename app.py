import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import Config
from projects.object_detection import obj_detect_model
from projects.face_expression import expression_model
from hub import allow_file
import tensorflow as tf
from PIL import Image
import numpy as np
from projects.object_detection.models.utils import visualization_utils
import cv2
import dlib
import base64
import json

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


@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        if file and allow_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Config.OBJ_UPLOAD_FOLDER, filename))
            return redirect(url_for('uploaded_file',filename=filename))
    except Exception as e:
        return redirect(url_for({"status":"error","message":""}))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        PATH_TO_TEST_IMAGES_DIR = Config.OBJ_UPLOAD_FOLDER
        TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR,filename.format(i)) for i in range(1, 2) ]
        IMAGE_SIZE = (12, 8)

        detection_graph, category_index = obj_detect_model.init_detection()

        with detection_graph.as_default():
            with tf.compat.v1.Session(graph=detection_graph) as sess:
                for image_path in TEST_IMAGE_PATHS:
                    image = Image.open(image_path)
                    image_np = obj_detect_model.convert_image_to_array(image)
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                    (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})
                    visualization_utils.visualize_boxes_and_labels_on_image_array(
                        image_np,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8)

                    im = Image.fromarray(image_np)
                    im.save(Config.OBJ_DETECTION_FOLDER + filename)

        return send_from_directory(Config.OBJ_DETECTION_FOLDER,
                                   filename)
    except Exception as e:
        return redirect({"status":"error","message":""})


# stock price

@app.route('/stock_prediction')
def stock_prediction():
    return render_template('stock_prediction.html')


# face recognition

@app.route('/face_recognize')
def face_recognize():
    return render_template('face_express_recognize.html')

CORS(app)

detector = dlib.get_frontal_face_detector()
model = expression_model.get_model()
model.load_weights(Config.EXPRESSION_MODEL)
Le = expression_model.load_object(Config.EXPRESSION_MODEL_LE)

@app.route('/expression_prediction', methods=['POST'])
def predict():
    # Decode video data sent from UI
    video_data = request.get_json()['video']
    video_data = video_data.split(',')[1]
    video_data = base64.b64decode(video_data)
    video_data = np.frombuffer(video_data, np.uint8)
    video = cv2.imdecode(video_data, cv2.IMREAD_COLOR)

    # Set up the video capture
    VideoCapture = cv2.VideoCapture(video)

    def generate():
        while True:
            # Capture frame from video
            ret, frame = VideoCapture.read()

            if not ret:
                yield jsonify({"error": "Failed to read frame from video."}), 500

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            rects = detector(gray, 0)

            if len(rects) >= 1:
                for rect in rects:
                    (x, y, w, h) = expression_model.rect_to_bb(rect)
                    img = gray[y - 10: y + h + 10, x - 10: x + w + 10]

                    if img.shape[0] == 0 or img.shape[1] == 0:
                        yield jsonify({"error": "Failed to extract face from frame."}), 500

                    else:
                        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
                        img = expression_model.ProcessImage(img)
                        out = expression_model.RealtimePrediction(img, model, Le)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        z = y - 15 if y - 15 > 15 else y + 15
                        cv2.putText(frame, str(out), (x, z), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                retval, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()

                # Send frame and prediction back to UI
                response = {'result': str(out)}
                data = {'image': base64.b64encode(frame_bytes).decode('utf-8'), 'prediction': json.dumps(response)}
                yield f"data: {json.dumps(data)}\n\n"

            else:
                retval, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()

                # Send frame and message back to UI
                response = {'result': 'No faces detected.'}
                data = {'image': base64.b64encode(frame_bytes).decode('utf-8'), 'prediction': json.dumps(response)}
                yield f"data: {json.dumps(data)}\n\n"

    return Response(generate(), mimetype='text/event-stream')



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