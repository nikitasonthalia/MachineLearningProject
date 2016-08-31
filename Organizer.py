##############################################################
# xgboost sklearn to train and test the model
# Author: Jinzhong Zhang
###############################################################

import csv, sys

if __name__ == '__main__':
    writer = csv.writer(open("submission1.csv", "w"))
    reader_res = csv.reader(open("submission.csv", "r"))
    results = {}
    irow = 0
    for row in reader_res:
        irow += 1
        try:
            results[int(row[0])]=int(row[1])
        except:
            print(row)
            pass
        if irow%1000==0:
            sys.stdout.write("\rRead {0} lines.".format(irow))
            sys.stdout.flush()

    sys.stdout.write("\n")
    reader = csv.reader(open("sample_submission.csv", "r"))
    irow = 0
    for row in reader:
        irow += 1
        if irow == 1:
            writer.writerow(row)
            continue
        query = int(row[0])
        result = int(results[query])
        if result<=0:
            print(query, result)
            result = 1
        writer.writerow([query, result])
