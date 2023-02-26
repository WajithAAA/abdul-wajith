import tensorflow as tf
from transformers import BertTokenizer, TFBertModel
import os
import pandas as pd
import numpy as np
import pickle

max_length = 20
batch_size = 16

with open('emotion_tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

model = tf.keras.models.load_model('emotion_model.h5',custom_objects={"TFBertModel": TFBertModel})

def bert_encode(data):
  tokens = tokenizer.batch_encode_plus(
    data, max_length=max_length, padding="max_length", truncation=True
  )
  return tf.constant(tokens["input_ids"])


def label(prediction):
  if prediction ==0:
    return "person is angry"
  elif prediction ==1:
    return "person is in fear"
  elif prediction ==2:
    return "person is in joy"
  elif prediction ==3:
    return "person is in love"
  elif prediction ==4:
    return "person is sad"
  else:
    return "person is surprise"

def predict(data):

  data_dic = {"text": data}
  x_data = pd.DataFrame(data_dic, index=[0])
  test_encoded = bert_encode(x_data)
  test_dataset = tf.data.Dataset.from_tensor_slices(test_encoded).batch(batch_size)

  predicted = model.predict(test_dataset, batch_size=batch_size)
  print(predicted)
  predicted_label = np.argmax(predicted, axis=-1)
  print(predicted_label)
  emotion = label(predicted_label)
  print(emotion)
  return emotion

data = "i feel bitchy but not defeated yet"
predict(data)

