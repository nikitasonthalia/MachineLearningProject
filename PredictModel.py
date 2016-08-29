##############################################################
# xgboost sklearn to train and test the model
# Author: Jinzhong Zhang
###############################################################

import xgboost as xgb
import csv, sys
import numpy as np
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.metrics import *
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

def evaluate(self, y, y_pred):
	''' this method is to evaluate accuracy of predict y given real y '''
	return sum(y==y_pred) / len(y)

if __name__ == '__main__':
    TRAIN_DATA = "MLprojectOutput/week345to6Formated/part-00000"
    TEST_DATA = "MLprojectOutput/week456to7Formated/part-00000"
    X, Y = readData(TRAIN_DATA, -1)
    X_Scaler = MinMaxScaler().fit(X)
    X = X_Scaler.transform(X)
    dtrain = xgb.DMatrix(X, label = Y)
    param = {'max_depth':4, 'eta':0.3, 'silent':0, 'objective':'reg:linear', 'nthread':4, 'eval_metric':'rmse'}
    __model = xgb.train(param.items(), dtrain)
    test_X, test_Y = readData(TEST_DATA, -1)
    test_X = X_Scaler.transform(test_X)
    dtest = xgb.DMatrix(test_X)
    Y_pred = list(map(lambda x: int(x), __model.predict(dtest)))
    writer = csv.writer(open("predict.csv", "w"))
    writer.writerows([Y_pred])
    #print(test_Y,Y_pred)
    print("R2=", r2_score(test_Y,Y_pred))
    print("Mean Squared Error=", mean_squared_error(test_Y,Y_pred))
#y_pred = np.array(list(map(lambda x: int(round(x)),y_pred)))
