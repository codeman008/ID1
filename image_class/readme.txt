msg: You can choose the following model to train your image,
and just switch in config.py:
VGG16,VGG19,InceptionV3,Xception,MobileNet,AlexNet,LeNet,ZF_Net,esNet18,ResNet34,ResNet50,ResNet_101,ResNet_152
主要根据keras库进行模型训练：https://keras.io/zh/applications/（keras应用中文文档）
train：
利用train.py进行训练，选择不同的模型可以取config.py进行选择。
模型主要包括：VGG16,VGG19,InceptionV3,Xception,MobileNet,AlexNet,LeNet,ZF_Net,esNet18,ResNet34,ResNet50,ResNet_101,ResNet_152
test:predict.py
利用predict.py进行模型预测，可以单张或批量
