import os

class Config:

    ROOT = os.getcwd()
    PROJECTS = os.path.join(ROOT, 'projects')
    OBJ_DETECTION   = os.path.join(PROJECTS, 'object_detection')

    OBJ_DETECT_MODEL_PATH = os.path.join(OBJ_DETECTION, 'models/ssd_model/frozen_inference_graph.pb')
    OBJ_DETECT_MODEL_LABELS = os.path.join(OBJ_DETECTION, 'models/data/mscoco_label_map.pbtxt')
    OBJ_DETECT_MODEL_CLASSES = 90
    OBJ_UPLOAD_FOLDER = os.path.join(OBJ_DETECTION, 'upload')
    OBJ_DETECTION_FOLDER = os.path.join(OBJ_DETECTION, 'detect_img/')

    ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])

    #EXPRESSION_MODEL = os.path.join(PROJECTS, 'face_expression/best_weights.h5')
    EXPRESSION_MODEL_LE = os.path.join(PROJECTS, 'face_expression/LabelEncoder.pck')


