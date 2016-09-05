# New-York-MTA-Optimization-System
This project help users choose the faster line in New York subway. It uses AWS machine learning model and Lambda function to predict the time to destination and send a meassage to users, telling them whether switch to express line or not. 

The code is just the sample code. We don't include our AWS key in it. If you want to run this code. Please add your AWS account ID, Identity pool ID and ROLE ARN into config.txt. 


Instruction of running:
python gatherData.py (collect data)
python buildTrainingDataSet.py new.csv(clean data)
python createAMLModel.py finalData.csv (build ML model)

Prediction using Lambda function need to be done on AWS page.
