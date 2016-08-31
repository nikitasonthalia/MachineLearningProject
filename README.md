# MachineLearningProject
Machine Learning for solving Inventory problem
### System Requirement
* CPU more than 6 cores
* Memory more than 16GB, prefer 32GB
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
sudo git clone --recursive https://github.com/dmlc/xgboost /opt/xgboost &&\
sudo cd /opt/xgboost &&\
sudo ./build.sh
export PYTHONPATH=/opt/xgboost/python-package:$PYTHONPATH
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


### Intall sbt
Install on Mac

<pre>
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install sbt
</pre>

Install on Linux

<pre>
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 642AC823
sudo apt-get update
sudo apt-get install sbt
</pre>

### Download the data from Kaggle
<pre>
wget https://www.kaggle.com/c/grupo-bimbo-inventory-demand/download/train.csv.zip
unzip train.csv.zip
</pre>

### Split Data
Run `./Splitter.sh train.csv`<br>
It probably takes half a day to finish. We did not optimize this part because we only need to run it once.

Now you should have `train_week[3-9].csv`. 

### Collect user information for a certain week
DataFormat folder contain the program for the formating and cleaning trainning dataset. It will format data userwise. All user data can be combine togther.
This will help us for making Co-Occurance matrix.
To Run this program on spark follow the following steps:
<pre>
    cd dataformat
    sbt package
    spark-submit ~/dataFormat/target/scala-2.10/spark-linecount_2.10-1.0.jar
</pre>
This will generate `week[3 to 9]objectoutput` output file in `MLPorjectOutput/` folder. 

### Make the Co-Occurance Matrix for product and depots.
Matrix folder contain scala program for making Co-Occurance Matrix. 
Follow the following steps to run.

<pre>
    cd Matrix
    sbt package
    spark-submit ~/dataFormat/target/scala-2.10/spark-linecount_2.10-1.0.jar
</pre>

Now you have Co-Occurance matrix for product in depot in MLProjectOutput folder. `Week[3 to 9]ProductMatrix` and `Week[3 to 9]DepotMatrix` file will be generated in  `MLProjectOutput/`  folder

### Calculate the popularity of products and depots
Run `spark-submit CalPopularity.py`
Now you should have `week[3-9]ProductPopularity/` and `week[3-9]DepotPopularity/` inside `MLprojectOutput/` directory.

### Build the Analytic Based Table
Change the `TRAIN_WEEKS` parameter in the `ABTBuilder.py` to the desired weeks. 

The default value is `TRAIN_WEEKS = [3,4,5,6,7,8]`. It means the program will use the demand of week8 as the target and use the user behaviors in weeks 3,4,5,6,7 as the features.

In this analysis, we only used `TRAIN_WEEKS = [3,4,5,6,7,8]` to generate `week34567to8Formated/` inside `MLprojectOutput/` directory to predict the next week and used `TRAIN_WEEKS = [3,4,5,6,7,9]` to generate `week34567to9Formated/` inside `MLprojectOutput/` directory to make the model to predict the next next week.

After you make the change, run `spark-submit ABTBuilder.py`
It usually takes 15-30 minutes to finish 4 weeks calculation. 

### Build the predictive model and validate
Choose the training data in `CreateModel.py`. The default ones are
<pre>
DATA = "MLprojectOutput/week34567to8Formated/part-00000" for "NextWeek"
DATA = "MLprojectOutput/week34567to9Formated/part-00000" for "NextNextWeek"
</pre>
In the code, using the API 
<pre>
    readData(filename, start_row, end_row)
</pre>
One can easily split the training and validation samples by specifying the row number.

Run `python3.4 CreateModel.py`

Now you should have `Predict_NextNextWeek_Scaler.pkl` and `Predict_NextWeek_Scaler.pkl` for normalizing the data and `PredictNextNextWeek.model` and `PredictNextWeek.model` as the models.

The validation test parameters are also displayed in this step so that you can always adjust your model based on it.

***The following instructions are only useful for real Kaggle submission***
### From Kaggle `test.csv` to `submission.csv`
   1. Run `./Splitter_Test.sh` to split the test data weekly. You should have `test_week10.csv` and `test_week11.csv`. This procedure takes several hours and only need to run once.
   2. Run `python3 TestABTBuilder.py` to build the ABT based on `test_week10.csv` and `test_week11.csv` queries. This script will retain the ID in test.csv. It takes serveral hours.
   3. Run `python3 Predict.py` to load the Scaler pkl files and the `PredictNextWeek.model` and `PredictNextNextWeek.model` and generate the `submission.csv`
   4. Submit the `submission.csv` to Kaggle and see the score
