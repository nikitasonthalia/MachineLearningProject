######################################
#   Spark Payroll Analysis           #
#   Author: Jinzhong Zhang           #
#   Aug, 2016                        #
######################################

# Plot colors
# b: blue
# g: green
# r: red
# c: cyan
# m: magenta
# y: yellow
# k: black
# w: white
import sys
from pyspark import SparkContext, SparkConf
from ast import literal_eval
import numpy as np

def parse(x):
    res = x[1:-1].split(',CompactBuffer')
    products = literal_eval(res[1][:-2]+',)')
    n_products = {}
    n_depots = {}
    for product in products:
        try:
            product_ID = product[2]
            depot_ID = product[0]
            demand = product[-1]
            if product_ID not in n_products:
                n_products[product_ID] = demand
            else:
                n_products[product_ID] += demand
            if depot_ID not in n_depots:
                n_depots[depot_ID] = demand
            else:
                n_depots[depot_ID] += demand
        except:
            sys.stdout.write("{0}\n".format(products))
            raise
    return (int(res[0]), n_products, n_depots)

def load_customer(filename):
    prod_dict={}
    depot_dict={}
    with open(filename, 'r') as f:
        lines = f.readlines()
        tot_lines = len(lines)
        iline = 0
        for line in lines:
            userID, products, depots = parse(line)
            prod_dict[userID] = products
            depot_dict[userID] = depots
            iline += 1
            if iline%1000==0:
                sys.stdout.write("\rRead {0}/{1} lines from {2}".format(iline, tot_lines, filename))
                sys.stdout.flush()
    sys.stdout.write("\n")
    return prod_dict, depot_dict

def load_occurrence_matrix(filename, item_dict={}):
    with open(filename, 'r') as f:
        lines = f.readlines()
        tot_lines = len(lines)
        iline = 0
        for line in lines:
            items, weight = line[1:-2].split(',')
            item1, item2 = items.split('#')
            item1 = int(item1)
            item2 = int(item2)
            weight = int(weight)
            # create a bi-direction search dictionary
            if item1 not in item_dict:
                item_dict[item1] = {item2:weight}
            elif item2 not in item_dict[item1]:
                item_dict[item1][item2] = weight
            else:
                item_dict[item1][item2] += weight

            if item2 not in item_dict:
                item_dict[item2] = {item1:weight}
            elif item1 not in item_dict[item2]:
                item_dict[item2][item1] = weight
            else:
                item_dict[item2][item1] += weight
            iline += 1
            if iline%1000==0:
                sys.stdout.write("\rRead {0}/{1} lines from {2}".format(iline, tot_lines, filename))
                sys.stdout.flush()
            # if iline>5: break
            # print (item_dict)
        sys.stdout.write("\n")
    return item_dict

# def build(userID, history):
#     res = []
#     for week in history:
#         res = week.lookup(userID)
#     sys.stdout.write("{0},{1}\n".format(userID,res))
#     return res

def sort_by_weight(prod_occurrence):
    ordered_occurrence = {}
    for userID, entry in prod_occurrence.items():
        weights = list(entry.values())
        sum_weights = sum(weights)
        weights = [weight*100/sum_weights for weight in weights ]
        occurrences = list(zip(list(entry.keys()),weights))
        occurrences.sort(key=lambda x:x[1], reverse=True)
        ordered_occurrence[userID] = occurrences
    return ordered_occurrence

N_TRAINING_WEEKS = 1
weeks_prod = [{}]*N_TRAINING_WEEKS
weeks_depot = [{}]*N_TRAINING_WEEKS
weeks_prod[0], weeks_depot[0] = load_customer("MLprojectOutput/week3objectoutput/part-00000")
prod_occurrence = load_occurrence_matrix("MLprojectOutput/week3Productmatrix/part-00000")
prod_occurrence = load_occurrence_matrix("MLprojectOutput/week4ProductMatrix/part-00000", prod_occurrence)
prod_occurrence = load_occurrence_matrix("MLprojectOutput/week5ProductMatrix/part-00000", prod_occurrence)
prod_occurrence = sort_by_weight(prod_occurrence)

MAX_RELATIVE_PRODUCTS = 3
def createSample(line):
    token = line.split(",")
    userID = token[4]
    product = token[5]
    depot = token[1]
    demand = int(token[-1][:-1])
    n_prod = [0]*N_TRAINING_WEEKS
    n_rel_prod = [[0]*MAX_RELATIVE_PRODUCTS]*N_TRAINING_WEEKS
    for i, week_prod in enumerate(weeks_prod):
        if userID in week_prod:
            if product in week_prod[userID]:
                n_prod[i] = week_prod[userID][product]
            if product in prod_occurrence:
                relative_prods = prod_occurrence[product]
                ifound = 0
                for j, rel_prod in enumerate(relative_prods):
                    if rel_prod[0] in week_prod[userID]:
                        n_rel_prod[i][ifound] = week_prod[userID][rel_prod]*rel_prod[1]
                        ifound += 1
                        if ifound==3:
                            break
    return n_prod+n_rel_prod[0]+[demand]

if __name__ == "__main__":
    if __debug__:
        count=0
        with open("train_week6.csv", 'r') as f:
            for line in f:
                print(createSample(line))
                count += 1
                if count>10:
                    break
    else:
        conf = SparkConf()
        sc = SparkContext(conf=conf)
        logger = sc._jvm.org.apache.log4j
        logger.LogManager.getLogger("org"). setLevel( logger.Level.WARN )
        logger.LogManager.getLogger("akka").setLevel( logger.Level.WARN )
        week6 = sc.textFile("train_week6.csv").map(createSample)
    # sys.stdout.write("{0}".format(week3.first()))
    #test.first().pprint()
