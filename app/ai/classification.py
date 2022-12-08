from io import BytesIO
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
# from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input

model = None

def load_model():
    # model = tf.keras.applications.MobileNetV2(weights="imagenet")
    # 從 HDF5 檔案中載入模型
    model = tf.keras.models.load_model('app/ai/model/EfficientNetV2B3_1128.h5')
    # model = tf.keras.models.load_model('app/ai/model/EfficientNetV2B3_1207_pb')
    # model = tf.saved_model.load('app/ai/model/EfficientNetV2B3.savedmodel')

    print("Model loaded")
    return model

def predict2(image: Image.Image):
    global model
    if model is None:
        model = load_model()

    infer = model.signatures["serving_default"]
    classes = ['asparagus', 'bambooshoots', 'betel', 'broccoli', 'cauliflower', 'chinesecabbage', 'chinesechives', 'custardapple', 'grape', 'greenhouse', 'greenonion', 'kale', 'lemon', 'lettuce', 'litchi', 'longan', 'loofah', 'mango', 'onion', 'others', 'papaya', 'passionfruit', 'pear', 'pennisetum', 'redbeans', 'roseapple', 'sesbania', 'soybeans', 'sunhemp', 'sweetpotato', 'taro', 'tea', 'waterbamboo']

    # img = Image.open(response.raw)
    img = image
    img = np.array(img)
    h, w = img.shape[:2]
    z = min(h, w)
    img = img[int(h/2)-int(z/2):int(h/2)+int(z/2), int(w/2)-int(z/2):int(w/2)+int(z/2)]
    img = cv2.resize(img, (224, 224))
    img = preprocess_input(img)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = img

    prediction_prob = infer(tf.constant(data))['softmax']
    pre = np.argmax(prediction_prob, axis=1)[0]
    result = classes[pre]
    print('預測結果為：', result)

    response = {
        "class" : result
    }
    return response

def predict(image: Image.Image):
    global model
    if model is None:
        model = load_model()

    image = np.asarray(image.resize((224, 224)))[..., :3]
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    # 預測
    preds = model.predict(image)
    # print( preds )

    # 顯示預測前2名的答案
    result = predictions(preds)
    # result = decode_predictions(preds, top=2)[0]

    response = []
    for i, res in enumerate(result):
        resp = {}
        resp["class"] = res[1]
        resp["confidence"] = f"{res[2]*100:0.2f} %"
        response.append(resp)
    return response
    # output :
    # [
    #   {'class': 'tea', 'confidence': '46.94 %'},
    #   {'class': 'custardapple', 'confidence': '30.80 %'}
    # ]

def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image

def predictions(preds):
    # sorting the predictions in descending order
    sorting = (-preds).argsort()
    # print( sorting )

    # getting the top 2 predictions
    sorted_ = sorting[0][:2]
    # print( sorted_ )

    # 總共32個分類
    classes = {'asparagus': 0, 'bambooshoots': 1, 'betel': 2, 'broccoli': 3, 'cauliflower': 4, 'chinesecabbage': 5, 'chinesechives': 6, 'custardapple': 7, 'grape': 8, 'greenhouse': 9, 'greenonion': 10, 'kale': 11, 'lemon': 12, 'lettuce': 13, 'litchi': 14, 'longan': 15, 'loofah': 16, 'mango': 17, 'onion': 18, 'others': 19, 'papaya': 20, 'passionfruit': 21, 'pear': 22, 'pennisetum': 23, 'redbeans': 24, 'roseapple': 25, 'sesbania': 26, 'soybeans': 27, 'sunhemp': 28, 'sweetpotato': 29, 'taro': 30, 'tea': 31, 'waterbamboo': 32}
    classes_list = [*classes.keys()]
    # print('classes_list', classes_list)

    results = []

    # predicted_index = classes index : 0 - 31
    for predicted_index in sorted_:
        predicted_label = classes_list[predicted_index]
        # print('predicted_index', predicted_index)

        item = []
        item.append(predicted_index)
        item.append(predicted_label)
        item.append(preds[0][predicted_index])
        # item[0] = predicted_index
        # item[1] = class
        # item[2] = confidence
        results.append(item)

        # rounding steps
        # prob = (preds[0][value]) * 100
        # prob = "%.2f" % round(prob,2)
        # print("I have %s%% sure that it belongs to %s." % (prob, predicted_label))
    return results
    # output :
    # [
    #   [31, 'tea', 0.46940377]
    #   [7, 'custardapple', 0.30798772]
    # ]
