import csv, sys
with open("predict.csv", 'r') as f_handle:
    reader = csv.reader(f_handle, delimiter=',', quotechar='"')
    pred = [ int(x) for x in next(reader) ]

data = []
with open("MLprojectOutput/week456to7Formated/part-00000", 'r') as f_handle:
    for row in f_handle:
        data.append(int(row[1:-2].split(',')[-1]))

errors = []
for i, v in enumerate(data):
    if v>0:
        errors.append(abs(v-pred[i])/v)
    else:
        errors.append(1.0 if pred[i]>0 else 0)
errors.sort()
print ("mean=",sum(errors)/len(pred))
print ("50 Percentile=", errors[int(len(pred)*0.5)], ", 75 Percentile=", errors[int(len(pred)*0.75)] )
