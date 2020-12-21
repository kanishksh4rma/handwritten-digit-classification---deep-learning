# -*- coding: utf-8 -*-
"""digit_recog

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TaBMpBSJ_GsXWUL7uzu6ZK0Q7H0z-Y7R
"""

from google.colab import drive
drive.mount('/content/gdrive')

!unzip -q "/content/gdrive/My Drive/handwritten-digits-data.zip"
!unzip -q "/content/gdrive/My Drive/digit_recog_model.zip"

import pandas as pd
from keras.datasets import mnist
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import warnings as war
war.filterwarnings('ignore')

'''

project name : handwritten digit classification --deep learning
author : @kanishksh4rma

'''

#load the data

(X_train,y_train),(X_test,y_test) = mnist.load_data()

#print the shape
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

#lets print the data

fig,ax = plt.subplots(5,5)
for i,axs in enumerate(ax.flat):
  axs.imshow(X_train[i],cmap='binary',interpolation = 'nearest')
  axs.set_xticks([])
  axs.set_yticks([])
  axs.axis('off')

"""# Deep learning"""

#import deep learning stuff

from keras.models import Sequential
from keras.layers import Dense, Activation, BatchNormalization,Dropout,Conv2D,MaxPooling2D,Flatten
from keras.utils.np_utils import to_categorical

# reshape dataset to have a single channel
X_train = X_train.reshape((X_train.shape[0], 28,28,1))
X_test = X_test.reshape((X_test.shape[0], 28, 28,1))

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

#one hot encoder for y
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

#create model

model = Sequential()
input_shape=(28,28,1)
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu',
                              input_shape=input_shape))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu',kernel_initializer='he_normal'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

#fit the model
model.fit(X_train,y_train,epochs=16)

#testify the validity

result = model.evaluate(X_test,y_test)
print('Accuracy : {} %'.format(round(result[1]*100,3)))

#save the model 
model.save('digit.h5')

df = pd.read_csv('train.csv')
df.head()

# train over train data

dataset = "/content/Images/train"
args={}
args["dataset"]=dataset
from imutils import paths
import argparse
import os
from skimage.transform import resize
import numpy as np
import cv2
img_paths = list(paths.list_images(args["dataset"]))  #image paths
t_data = []
label =  []
for path in img_paths:
    
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (_, image) = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    resize(image, (28, 28, 1))
    t_data.append(image)
    

t_data = np.array(t_data) / 255.0
t_data = t_data.reshape((-1, 28,28,1))

from sklearn.model_selection import train_test_split

X_train = t_data
y_train = df.label

'''# reshape dataset to have a single channel
X_train = X_train.reshape((X_train.shape[0], 28,28,3))

X_train = X_train.astype('float32')
X_train /= 255

'''  # for now
#one hot encoder for y
from keras.utils.np_utils import to_categorical

y_train = to_categorical(y_train)

'''import keras
model = keras.models.load_model('digit.h5')
model.fit(X_train,y_train,epochs=15)

model.save('digit2.h5')
'''
'''# import the test data

from google.colab import drive
drive.mount('/content/gdrive')

!unzip -q "/content/gdrive/My Drive/Test.zip"'''

dataset = "/content/Images/test"
args={}
args["dataset"]=dataset

from imutils import paths
import argparse
import os
from skimage.transform import resize
import numpy as np
import cv2


img_paths = list(paths.list_images(args["dataset"]))  #image paths
data = []
label =  []
for path in img_paths:
    labels = path.split(os.path.sep)[-1]   #split the image paths to get the img name
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (_, image) = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)  #convert black to white and vice-versa
    resize(image, (28, 28, 1))
    data.append(image)
    label.append(labels)

data = np.array(data) / 255.0           # data normalization  
labels = np.array(labels)         
data = data.reshape((-1, 28,28,1))

import keras
model = keras.models.load_model('digit.h5')   # import our created model
my_pred = model.predict(data)

predicted_label = np.argmax(my_pred,axis=1)
pre_df = pd.DataFrame(label,columns=['filename'])
pre_df['label'] = pd.DataFrame(predicted_label)
pre_df.column = ['filename','label']

pre_df.head()

pre_df.to_csv('output3.csv',index=False)

