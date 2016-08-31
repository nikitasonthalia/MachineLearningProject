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
ValidateWeek = "NextWeek"
if ValidateWeek != "NextWeek" and ValidateWeek != "NextNextWeek":
    raise ValueError(ValidateWeek)

def readData(filename, nrow=100):
    irow = 0
    data = []
    with open(filename, 'r') as f_handle:
        for row in f_handle:
            data.append([np.float64(x) for x in row[1:-2].split(',')])
            irow += 1
            if irow%1000==0:
                sys.stdout.write("\rRead {0} lines from {1}".format(irow, filename))
                sys.stdout.flush()
            if irow>=nrow and nrow>0:
                break
    data = np.array(data)
    X = data[:,:-1]
    Y = data[:,-1]
    return (X,Y)

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

if __name__ == '__main__':
    DATA = "MLprojectOutput/week34567to8Formated/part-00000"
    X_TEST, Y_TEST = readData(DATA, 100)
    X_Scaler = joblib.load('Predict{0}_Scaler.pkl'.format(ValidateWeek))
    __model = xgb.Booster({'nthread':4}) #init model
    __model.load_model("Predict{0}.model".format(ValidateWeek)) # load data
    X_TEST = X_Scaler.transform(X_TEST)
    dtest = xgb.DMatrix(X_TEST)
    Y_pred = list(map(lambda x: int(x), __model.predict(dtest)))
    evaluate(Y_TEST,Y_pred)
