# -*- coding: utf-8 -*-
import sys
class DefaultConfig():
    model_name = 'ResNet152'#sys.argv[1]

    train_data_path = './dataset/train/'
    test_data_path = './dataset/test/'
    checkpoints = './checkpoints/'
    channles = 1

    if model_name == 'InceptionV3':
        normal_size = 75
    elif model_name == 'Xception':
        normal_size = 71
    elif model_name == 'DenseNet':
        normal_size = 128
    else:
        normal_size = 64

    epochs = 100
    batch_size = 128
    data_augmentation = True
    classes = 2
    lr = 0.001
    default_optimizers = False
    monitor = 'val_loss'
    lr_reduce_patience = 5 #需要降低学习率的训练步长
    early_stop_patience = 10  #提前终止训练的步长

    cut = False
    rat = 0.1#if cut,img[slice(h*self.rat,h-h*self.rat),slice(w*self.rat,w-w*self.rat)]

config = DefaultConfig()
