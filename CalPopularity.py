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

def parser(line, i):
    tokens=line.split(',')
    # sys.stdout.write("{0}".format(tokens))
    return (int(tokens[i]), int(tokens[-1]))

if __name__ == "__main__":
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel( logger.Level.WARN )
    logger.LogManager.getLogger("akka").setLevel( logger.Level.WARN )
    for i in range(3,10):
        prod = sc.textFile("train_week{0}.csv".format(i)).map(lambda line:parser(line,5)).reduceByKey(lambda a, b: a + b)
        prod.coalesce(1).saveAsTextFile("MLprojectOutput/week{0}ProductPopularity".format(i))
        depot = sc.textFile("train_week{0}.csv".format(i)).map(lambda line:parser(line,1)).reduceByKey(lambda a, b: a + b)
        depot.coalesce(1).saveAsTextFile("MLprojectOutput/week{0}DepotPopularity".format(i))
    # sys.stdout.write("{0}".format(week3.first()))
    #test.first().pprint()
