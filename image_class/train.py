"""
msg: You can choose the following model to train your image, and just switch in config.py:
    VGG16,VGG19,InceptionV3,Xception,MobileNet,AlexNet,LeNet,ZF_Net,esNet18,ResNet34,ResNet50,ResNet_101,ResNet_152
"""

from __future__ import print_function
from config import config
import numpy as np
import os,glob,itertools,tqdm,cv2,keras
from random import shuffle
from sklearn.preprocessing import OneHotEncoder

from keras.preprocessing.image import img_to_array,ImageDataGenerator
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.callbacks import TensorBoard

import tensorflow as tf
config1 = tf.ConfigProto()
config1.gpu_options.allow_growth = True
tf.Session(config=config1)

# from keras.backend.tensorflow_backend import set_session
# import tensorflow as tf
# config_yolo = tf.ConfigProto()
# config_yolo.gpu_options.per_process_gpu_memory_fraction = 0.15
# set_session(tf.Session(config=config_yolo))

import sys
sys.setrecursionlimit(10000)

from Build_model import Build_model

class Train(Build_model):
    def __init__(self,config):
        # super(Build_model,self).__init__(config)
        Build_model.__init__(self,config)

    def get_file(self,path):
        ends = os.listdir(path)[0].split('.')[-1]
        img_list = glob.glob(path + '/*.'+ends)

        return img_list

    def load_data(self):
        categories = list(map(self.get_file, list(map(lambda x: self.train_data_path + x, os.listdir(self.train_data_path)))))
        data_list = list(itertools.chain.from_iterable(categories))
        shuffle(data_list)
        images_data ,labels= [],[]

        for file in tqdm.tqdm(data_list):
            if self.channles == 3:
                img = cv2.imread(file)
                # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                # img = cv2.threshold(img,128,255,cv2.THRESH_BINARY)[-1]
                _, w, h = img.shape[::-1]
            else:
                # img=cv2.threshold(cv2.imread(file,0), 128, 255, cv2.THRESH_BINARY)[-1]
                img = cv2.imread(file,0)
                # img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[-1]
                w, h = img.shape[::-1]



            if self.cut:
                img = img[slice(int(h*self.rat),int(h-h*self.rat)),slice( int(w*self.rat),int(w-w*self.rat) )]

            img = cv2.resize(img,(self.normal_size,self.normal_size))
            label = file.split('/')[3][0]
            print('img:',file,' has label:',label)
            img = img_to_array(img)
            images_data.append(img)
            labels.append(label)
            # print(type(images_data))

        images_data = np.array(images_data, dtype='float')/255.0
        #print(np.array(labels))
        #labels = to_categorical(np.array(labels),num_classes=self.classes)
        labels = np.array(labels).reshape(len(labels), -1)
        enc = OneHotEncoder()
        enc.fit(labels)
        labels = enc.transform(labels).toarray()
        print(labels)

        print(np.array(labels))
        X_train, X_test, y_train, y_test = train_test_split(images_data,labels)
        return X_train, X_test, y_train, y_test

    def mkdir(self,path):
        if not os.path.exists(path):
            return os.mkdir(path)
        return path

    def train(self,X_train, X_test, y_train, y_test,model):
        tensorboard=TensorBoard(log_dir=self.mkdir(self.checkpoints+self.model_name))

        lr_reduce = keras.callbacks.ReduceLROnPlateau(monitor=config.monitor,
                                                      factor=0.1,
                                                      patience=config.lr_reduce_patience,
                                                      verbose=1,
                                                      mode='auto',
                                                      cooldown=0)
        early_stop = keras.callbacks.EarlyStopping(monitor=config.monitor,
                                                   min_delta=0,
                                                   patience=config.early_stop_patience,
                                                   verbose=1,
                                                   mode='auto')
        checkpoint = keras.callbacks.ModelCheckpoint(self.mkdir(self.checkpoints+self.model_name)+'/'+self.model_name+'.h5',
                                                     monitor=config.monitor,
                                                     verbose=1,
                                                     save_best_only=True,
                                                     save_weights_only=True,
                                                     mode='auto',
                                                     period=1)

        if self.data_augmentation:
            print("using data augmentation method")

            data_aug = ImageDataGenerator(
                rotation_range=5,  # 图像旋转的角度
                width_shift_range=0.2,  # 左右平移参数
                height_shift_range=0.2,  # 上下平移参数
                zoom_range=0.3,  # 随机放大或者缩小
                horizontal_flip=True,  # 随机翻转
            )

            data_aug.fit(X_train)
            model.fit_generator(
                data_aug.flow(X_train, y_train, batch_size=config.batch_size),
                steps_per_epoch=X_train.shape[0] // self.batch_size,
                validation_data=(X_test, y_test),
                shuffle=True,
                epochs=self.epochs, verbose=1, max_queue_size=1000,
                callbacks=[early_stop,checkpoint,lr_reduce,tensorboard],
            )
        else:
            print('\nmodel=\n',model)
            model.fit(x=X_train,y=y_train,
                      batch_size=self.batch_size,
                      validation_data=(X_test,y_test),
                      epochs=self.epochs,
                      callbacks=[early_stop,checkpoint,lr_reduce,tensorboard],
                      shuffle=True,
                      verbose=1)


    def start_train(self):
        X_train, X_test, y_train, y_test=self.load_data()
        model = Build_model(config).build_model()
        self.train(X_train, X_test, y_train, y_test,model)

    def remove_logdir(self):
        print(os.system('ls checkpoints/'+self.model_name+'/'+'events*'))
        os.system('rm checkpoints/'+self.model_name+'/'+'events*')

def main():
    train = Train(config)
    train.remove_logdir()
    train.start_train()
    print('Done')


if __name__=='__main__':
    main()
