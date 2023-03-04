import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential, Model
from keras.layers import Dense, RepeatVector, TimeDistributed
from keras.layers import LSTM, Dropout, BatchNormalization, Input
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import scipy.stats
from datetime import datetime, timedelta
import tensorflow as tf

def processData(data,lb,la):
    X,Y = [],[]
    for i in range(len(data)):
        if i+lb+la < len(data):
            X.append(data[i:(i+lb),0])
            Y.append(data[(i+lb):(i+lb+la),0])
    return np.array(X),np.array(Y)

#model 1
def get_singular_model(lb):
    model = Sequential()
    model.add(LSTM(64,input_shape=(lb,1)))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam',loss='mse')
    
    return model
  
 
#model 2
def get_enc_dec_model(lb, la):
    encoder_inputs = Input(shape=(lb, 1))
    encoder_l1 = LSTM(16, activation='relu', return_state=True)
    encoder_outputs1 = encoder_l1(encoder_inputs)

    encoder_states1 = encoder_outputs1[1:]

    decoder_inputs = RepeatVector(la)(encoder_outputs1[0])
    decoder_l1 = LSTM(16, activation='relu', return_sequences=True)(decoder_inputs, initial_state = encoder_states1)
    decoder_outputs1 = TimeDistributed(Dense(1))(decoder_l1)

    model = Model(encoder_inputs,decoder_outputs1)
    model.compile(loss='mse', optimizer='adam')
    
    return model

def get_data(df, lb, la):
    cl = df.close[1:]
    train = cl[1:]
    scl = MinMaxScaler()
    scl.fit(train.values.reshape(-1,1))
    cl = scl.transform(cl.values.reshape(-1,1))
    
    X,y = processData(cl,lb,la)
    X_train,X_test = X[:int(X.shape[0]*0.90)],X[int(X.shape[0]*0.90):]
    y_train,y_test = y[:int(y.shape[0]*0.90)],y[int(y.shape[0]*0.90):]
    
    X_train = X_train.reshape((X_train.shape[0],X_train.shape[1],1))
    X_test = X_test.reshape((X_test.shape[0],X_test.shape[1],1))
    y_train = y_train.reshape((y_train.shape[0],y_train.shape[1],1))
    y_test = y_test.reshape((y_test.shape[0],y_test.shape[1],1))
    
    return scl, X_train, X_test, y_train, y_test
  
lb, la = 20, 1
scl, X_train, X_test, y_train, y_test = get_data(df, lb, la)
singular_model = get_singular_model(lb)
singular_model.fit(X_train, y_train, epochs=10, validation_data=(X_test,y_test), shuffle=False)

lb, la = 20, 20
scl, X_train, X_test, y_train, y_test = get_data(df, lb, la)
enc_dec_model = get_enc_dec_model(lb, la)
enc_dec_model.fit(X_train, y_train, epochs=20, validation_data=(X_test,y_test), shuffle=False)
