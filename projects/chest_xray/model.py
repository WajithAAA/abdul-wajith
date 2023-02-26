import tensorflow as tf
import pathlib
import numpy as np

# Define the path to the saved model
model_path = pathlib.Path('xray_model.h5')

test_image_path = 'test_img\IM-0001-0001.jpeg'

model = tf.keras.models.load_model(model_path)

# Define a function to preprocess the input image
def preprocess_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [224, 224])
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    return np.expand_dims(image, axis=0)

# Preprocess the input image
test_image = preprocess_image(test_image_path)

# Make a prediction on the input image
prediction = model.predict(test_image)
print(prediction)
# Print the prediction
if prediction  < 0.5:
    print('The image is NORMAL')
else:
    print('The image is PNEUMONIA')

