##############################################################
# xgboost sklearn to train and test the model
# Author: Jinzhong Zhang
###############################################################

import xgboost as xgb
import csv, sys, math
import numpy as np
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.metrics import *
from sklearn.externals import joblib

def readData(filename, start_row=0, end_row=-1):
    irow = -1
    data = []
    with open(filename, 'r') as f_handle:
        for row in f_handle:
            irow += 1
            if irow<start_row:
                continue
            elif irow>end_row and end_row>0:
                break
            data.append([np.float64(x) for x in row[1:-2].split(',')])
            if irow%1000==0:
                sys.stdout.write("\rRead {0} lines from {1}".format(irow, filename))
                sys.stdout.flush()
    data = np.array(data)
    return (data[:,:-1],data[:,-1])

def evaluate(data, pred):
    print("R2=", r2_score(data,pred))
    print("Mean Squared Error=", mean_squared_error(data,pred))
    errors = []
    sum_ = 0
    total_ = 0
    for i, v in enumerate(data):
        if v>0:
            errors.append(abs(v-pred[i])/v)
        else:
            errors.append(1.0 if pred[i]>0 else 0)
        sum_ += errors[-1]**2
        total_ += v-pred[i]
    errors.sort()
    print ("mean=",math.sqrt(sum_/len(pred)))
    print ("total=",total_)
    print ("50 Percentile=", errors[int(len(pred)*0.5)], ", 75 Percentile=", errors[int(len(pred)*0.75)] )
    print ("90 Percentile=", errors[int(len(pred)*0.9)], ", 99.5 Percentile=", errors[int(len(pred)*0.995)] )

def train(mode):
    if mode == "NextWeek":
        DATA = "MLprojectOutput/week34567to8Formated/part-00000"
    else:
        DATA = "MLprojectOutput/week34567to9Formated/part-00000"
    X, Y = readData(DATA, 10000, -1)
    X_Scaler = MinMaxScaler().fit(X)
    joblib.dump(X_Scaler, 'Predict{0}_Scaler.pkl'.format(mode))
    X = X_Scaler.transform(X)
    dtrain = xgb.DMatrix(X, label = Y)
    param = { 'booster':"gbtree",
              'eta':0.3,
              'max_depth':6,
              'subsample':0.85,
              'colsample_bytree':0.7,
              'silent':0,
              'objective':'reg:linear',
              'nthread':10,
              'eval_metric':'rmse'}
    __model = xgb.train(param.items(), dtrain)
    __model.save_model('Predict{0}.model'.format(mode))
    X_TEST, Y_TEST = readData(DATA, 0, 10000)
    X_TEST = X_Scaler.transform(X_TEST)
    dtest = xgb.DMatrix(X_TEST)
    Y_pred = list(map(lambda x: int(x), __model.predict(dtest)))
    evaluate(Y_TEST,Y_pred)

if __name__ == '__main__':
    train('NextWeek')
    train('NextNextWeek')
