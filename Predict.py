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
PredictWeek = "NextNextWeek"
if PredictWeek != "NextWeek" and PredictWeek != "NextNextWeek":
    raise ValueError(PredictWeek)

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
    ID = data[:,0].astype(int)
    X = data[:,1:]
    return (ID, X)

def evaluate(self, y, y_pred):
	''' this method is to evaluate accuracy of predict y given real y '''
	return sum(y==y_pred) / len(y)

if __name__ == '__main__':
    TEST_DATA = "MLprojectOutput/week56789to11Formated/part-00000"
    IDs, test_X = readTestData(TEST_DATA, -1)
    X_Scaler = joblib.load('Predict{0}_Scaler.pkl'.format(PredictWeek))
    __model = xgb.Booster({'nthread':4}) #init model
    __model.load_model("Predict{0}.model".format(PredictWeek)) # load data
    test_X = X_Scaler.transform(test_X)
    dtest = xgb.DMatrix(test_X)
    Y_pred = list(map(lambda x: int(x), __model.predict(dtest)))
    writer = csv.writer(open("predict_week11.csv", "w"))
    writer.writerows(zip(IDs, Y_pred))
