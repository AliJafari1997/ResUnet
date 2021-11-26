import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import numpy as np
from glob import glob
import cv2
import tensorflow as tf
from tensorflow.keras.callbacks import *
from data import load_data,tf_dataset
from model import build_model
from tensorflow.keras.metrics import *
from tensorflow.keras.utils import CustomObjectScope
from utils import *
from metrics import *

if __name__=='__main__':
    path= 'CVC-ClinicDB'
    (train_x,train_y),(valid_x,valid_y),(test_x,test_y)=load_data(path)
    print(len(train_x),len(valid_x),len(test_x))

    # hyperparameters
    batch=8
    lr=1e-4
    epochs=5


    train_dataset=tf_dataset(train_x,train_y,batch=batch)
    valid_dataset=tf_dataset(valid_x,valid_y,batch=batch)

    opt = tf.keras.optimizers.Adam(lr)
    metrics=['acc',Recall(),Precision(),iou]

    callbacks=[
        ModelCheckpoint('.\\files\\model.h5'),
        ReduceLROnPlateau(monitor='val_loss',factor=0.1,patience=3),
        CSVLogger('.\\files\\data.csv',append=True),
        TensorBoard(),
        EarlyStopping(monitor='val_loss',patience=10,restore_best_weights=False)
    ]


    train_steps=len(train_x)//batch
    valid_steps=len(valid_x)//batch

    if len(train_x) % batch != 0:
        train_steps += 1

    if len(valid_x) % batch != 0:
        valid_steps += 1

    model = load_model_weight("C:\\Users\\PC\\Desktop\\polyp_segmentation\\files\\model.h5")
    model.compile(loss="binary_crossentropy", optimizer=opt, metrics=['acc',Recall(),Precision(),iou])

    model.fit(train_dataset,
        validation_data=valid_dataset,
        epochs=epochs,
        steps_per_epoch=train_steps,
        validation_steps=valid_steps,
        callbacks=callbacks)