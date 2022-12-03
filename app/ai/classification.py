from io import BytesIO

import numpy as np
import tensorflow as tf
from PIL import Image
# from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.applications.efficientnet_v2 import decode_predictions

model = None

def load_model():
    # model = tf.keras.applications.MobileNetV2(weights="imagenet")
    # 從 HDF5 檔案中載入模型
    model = tf.keras.models.load_model('app/ai/model/EfficientNetV2B3_1128.h5')

    print("Model loaded")
    return model


def predict(image: Image.Image):
    global model
    if model is None:
        model = load_model()

    image = np.asarray(image.resize((224, 224)))[..., :3]
    image = np.expand_dims(image, 0)
    image = image / 127.5 - 1.0

    result = decode_predictions(model.predict(image), 2)[0]

    response = []
    for i, res in enumerate(result):
        resp = {}
        resp["class"] = res[1]
        resp["confidence"] = f"{res[2]*100:0.2f} %"

        response.append(resp)

    return response

def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image
