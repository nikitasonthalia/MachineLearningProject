##############################################################
# xgboost sklearn to train and test the model
# Author: Jinzhong Zhang
###############################################################

import xgboost as xgb
import csv, sys
import numpy as np
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.metrics import *
from sklearn.externals import joblib

def readTestData(filename, nrow=100):
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
    sys.stdout.write("\n")
    return (data[:,0].astype(int), data[:,1:])

def reformat(pred):
    y=int(pred)
    if y<0:
        y=0
    return y

def predict(DATA, mode):
    IDs, test_X = readTestData(DATA, -1)
    X_Scaler = joblib.load('Predict{0}_Scaler.pkl'.format(mode))
    __model = xgb.Booster({'nthread':4}) #init model
    __model.load_model("Predict{0}.model".format(mode)) # load data
    test_X = X_Scaler.transform(test_X)
    dtest = xgb.DMatrix(test_X)
    return (IDs, list(map(lambda x: reformat(x), __model.predict(dtest))))

if __name__ == '__main__':
    IDs_1, pred_1 = predict("MLprojectOutput/week56789to10Formated/part-00000","NextWeek")
    IDs_2, pred_2 = predict("MLprojectOutput/week56789to11Formated/part-00000","NextWeek")
    writer = csv.writer(open("submission.csv", "w"))
    writer.writerow(['id','Demanda_uni_equil'])
    writer.writerows(zip(np.append(IDs_1,IDs_2), pred_1+pred_2))
