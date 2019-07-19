"""
author:zhouwen
msg: ID class
"""
from __future__ import print_function
from config import config
import sys
import cv2
import os
from keras.preprocessing.image import img_to_array
import numpy as np
import tensorflow as tf

config1 = tf.ConfigProto()
config1.gpu_options.allow_growth = True
tf.Session(config=config1)

from Build_model import Build_model


class PREDICT(Build_model):
    def __init__(self, config):
        Build_model.__init__(self, config)
        self.test_data_path = config.test_data_path

    def Predict(self):
        model = Build_model(self.config).build_model()
        model.load_weights(self.checkpoints + '/' + self.model_name + '/' + self.model_name + '.h5')
        print(self.checkpoints + '/' + self.model_name + '/' + self.model_name + '.h5')
        data_list = []
        for x in os.listdir(self.test_data_path):
            path = os.path.join(self.test_data_path, x)
            img_ = cv2.imread(path, int(self.channles / 3))
            if img_ is None:
                print(path)
                continue
            data_list.append([cv2.resize(img_, (self.normal_size, self.normal_size)), path])
        i, j, tmp = 0, 0, []
        for imgs in data_list:
            img = imgs[0]
            img = np.array([img_to_array(img)], dtype='float') / 255.0
            pred = model.predict(img).tolist()[0]
            label = pred.index(max(pred))
            confidence = max(pred)
            if label == 0 and confidence>0.95:
                print(imgs[1], confidence)


def main():
    predict = PREDICT(config)
    predict.Predict()


if __name__ == '__main__':
    main()
