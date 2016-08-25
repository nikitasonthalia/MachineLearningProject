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

# def sort_by_weight(prod_occurrence):
#     ordered_occurrence = {}
#     for userID, entry in prod_occurrence.items():
#         weights = list(entry.values())
#         # sum_weights = sum(weights)
#         # weights = [weight*100/sum_weights for weight in weights ]
#         occurrences = list(zip(list(entry.keys()),weights))
#         occurrences.sort(key=lambda x:x[1], reverse=True)
#         ordered_occurrence[userID] = occurrences
#     return ordered_occurrence

def load_popularity(filename, item_pop={}):
    with open(filename, 'r') as f:
        for line in f:
            item, pop = line[1:-2].split(', ')
            item = int(item)
            if item not in item_pop:
                item_pop[item] = int(pop)
            else:
                item_pop[item] += int(pop)
    sys.stdout.write("Read popularity from {0}, done.\n".format(filename))
    return item_pop

N_TRAINING_WEEKS = 2
weeks_prod = [{}]*N_TRAINING_WEEKS
weeks_depot = [{}]*N_TRAINING_WEEKS
# weeks_prod[0], weeks_depot[0] = load_customer("test")
# weeks_prod[1], weeks_depot[1] = load_customer("test")
weeks_prod[0], weeks_depot[0] = load_customer("MLprojectOutput/week3objectoutput/part-00000")
weeks_prod[1], weeks_depot[1] = load_customer("MLprojectOutput/week4objectoutput/part-00000")
weeks_prod[1], weeks_depot[1] = load_customer("MLprojectOutput/week5objectoutput/part-00000")

prod_occurrence = load_occurrence_matrix("MLprojectOutput/week3ProductMatrix/part-00000")
prod_occurrence = load_occurrence_matrix("MLprojectOutput/week4ProductMatrix/part-00000", prod_occurrence)
prod_occurrence = load_occurrence_matrix("MLprojectOutput/week5ProductMatrix/part-00000", prod_occurrence)
# prod_occurrence = sort_by_weight(prod_occurrence)

product_popularity = load_popularity("MLprojectOutput/week3ProductPopularity/part-00000")
product_popularity = load_popularity("MLprojectOutput/week4ProductPopularity/part-00000", product_popularity)
product_popularity = load_popularity("MLprojectOutput/week5ProductPopularity/part-00000", product_popularity)

depot_popularity = load_popularity("MLprojectOutput/week3DepotPopularity/part-00000")
depot_popularity = load_popularity("MLprojectOutput/week4DepotPopularity/part-00000", depot_popularity)
depot_popularity = load_popularity("MLprojectOutput/week5DepotPopularity/part-00000", depot_popularity)

MAX_RELATIVE_PRODUCTS = 3
def createSample(line):
    token = line.split(",")
    userID = int(token[4])
    product = int(token[5])
    depot = int(token[1])
    demand = int(token[-1][:-1])
    n_prod = [0]*N_TRAINING_WEEKS
    n_rel_prod = [[]]*N_TRAINING_WEEKS
    for i, week_prod in enumerate(weeks_prod):
        if userID in week_prod:
            shopping_list = week_prod[userID]
            if product in shopping_list:
                n_prod[i] = shopping_list[product]
            if product in prod_occurrence:
                relative_prods = prod_occurrence[product]
                for prod, number in shopping_list.items():
                    if prod in relative_prods:
                        n_rel_prod[i].append(relative_prods[prod]*number)
            n_rel_prod[i].sort(reverse=True)
            n = len(n_rel_prod[i])
            if n > MAX_RELATIVE_PRODUCTS:
                n_rel_prod[i]=n_rel_prod[i][:MAX_RELATIVE_PRODUCTS]
            else:
                n_rel_prod[i].extend([0]*(MAX_RELATIVE_PRODUCTS-n))
    row = []
    for i, entry in enumerate(n_prod):
        row.append(entry)
        row.extend(n_rel_prod[i])
    #calculate the popularities
    if product in product_popularity:
        prod_pop = product_popularity[product]
    else:
        prod_pop = 0
    if depot in depot_popularity:
        depot_pop = depot_popularity[depot]
    else:
        depot_pop = 0
    row.extend([prod_pop,depot_pop,demand])
    return row

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
