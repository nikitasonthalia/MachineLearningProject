# MachineLearningProject
Machine Learning for solving Inventory problem
### Download the code
<pre>
git clone https://github.com/nikitasonthalia/MachineLearningProject.git
cd MachineLearningProject
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
Now you should have __train_week3.csv__ to __train_week9.csv__. 

### Collect user information for a certain week
DataFormat folder contain the program for the formating and cleaning trainning dataset. It will format data userwise. All user data can be combine togther.
This will help us for making Co-Occurance matrix.

To run this follow the above steps.
### Make the Co-Occurance Matrix for product and depots.
To Run that on Sprak Follow the Following steps:
Step 1 : Create Jar file for this program.
Step 2 : Open terminal in Sprak evniroment.
step 3 : goto in bin folder of spark.
step 4 : run script spark-submit with the jar path given as arugment.
step 5 : done

This way you can create the Co-Occurance matrix.

To create the jar follow the followig steps:
Step 1: Open terminal in the Matrix program folder.
Step 2: write sbt command.
Step 3: write package command.
step4 : done

### Calculate the popularity of products and depots
Run `spark-submit CalPopularity.py`
Now you should have `week[3-9]ProductPopularity/` and `week[3-9]DepotPopularity/` inside `MLprojectOutput/` directory.

### Build the Analytic Based Table
Run `spark-submit ABTBuilder.py`
