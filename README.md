# MachineLearningProject
Machine Learning for solving Inventory problem
### System Requirement
* CPU more than 6 cores
* Memory more than 16GB
* Disk more than 50GB
* Operating System: Ubuntu 15.10 Wily
* Python 3.x

### Download the code
<pre>
git clone https://github.com/nikitasonthalia/MachineLearningProject.git
cd MachineLearningProject
</pre>

### Install XGBOOST
<pre>
git clone --recursive https://github.com/dmlc/xgboost /opt/xgboost &&\
    cd /opt/xgboost &&\
    ./build.sh
</pre>

### Install numpy, scipy, and scikit-learn
<pre>
sudo pip3 install numpy==1.11.0 scipy==0.17.0 sklearn
</pre>
    
### Install Spark
<pre>
wget http://d3kbcqa49mib13.cloudfront.net/spark-2.0.0-bin-hadoop2.7.tgz
tar -xvf spark-2.0.0-bin-hadoop2.7.tgz -C /opt/
export PATH=$PATH:/opt/spark-2.0.0-bin-hadoop2.7/bin/
</pre>

### Download the data from Kaggle
<pre>
wget https://www.kaggle.com/c/grupo-bimbo-inventory-demand/download/train.csv.zip
unzip train.csv.zip
</pre>

### Split Data
Run `./Splitter.sh train.csv`<br>
It probably takes half a day to finish. We did not optimize this part because we only need to run it once.
Now you should have __train_week3.csv__ to __train_week9.csv__. 

### Collect user information for a certain week
DataFormat folder contain the program for the formating and cleaning trainning dataset. It will format data userwise. All user data can be combine togther.
This will help us for making Co-Occurance matrix.
To Run this program on spark follow the following steps:

Step 1: Open terminal in the dataFormat program folder.
Step 2: write sbt.
Step 3: write package.
This will generate jar in Dataformat folder. 
Step 4 : Open terminal in Sprak folder.
step 5 : goto in bin folder of spark.
step 6 : ./spark-submit dataFormat.jar
step 7: done

### Make the Co-Occurance Matrix for product and depots.
Matrix folder contain scala program for making Co-Occurance Matrix. 
Follow the following steps to run.

Step 1: Open terminal in the Matrix program folder.
Step 2: write sbt.
Step 3: write package.
This will generate jar in Matrix folder. 
Step 4 : Open terminal in Sprak folder.
step 5 : goto in bin folder of spark.
step 6 : ./spark-submit matrix.jar
step 7: done

Now you have Co-Occurance matrix for week[3] of product. 
You can make changes for product and depot matrix and generate output. 
Changes can be done in input file only. 

### Calculate the popularity of products and depots
Run `spark-submit CalPopularity.py`
Now you should have `week[3-9]ProductPopularity/` and `week[3-9]DepotPopularity/` inside `MLprojectOutput/` directory.

### Build the Analytic Based Table
Change the `TRAIN_WEEKS` parameter in the `ABTBuilder.py` to the desired weeks. 

The default value is `TRAIN_WEEKS = [3,4,5,6]`. It means the program will use the demand of week6 as the target and use the user behaviors in weeks 3,4,5 as the features.

In this analysis, we only used `TRAIN_WEEKS = [3,4,5,6]` to generate `week345to6Formated/` inside `MLprojectOutput/` directory as training data and used `TRAIN_WEEKS = [4,5,6,7]` to generate `week456to7Formated/` inside `MLprojectOutput/` directory as testing data.

After you make the change, run `spark-submit ABTBuilder.py`
It usually takes 15-30 minutes to finish 4 weeks calculation. 
