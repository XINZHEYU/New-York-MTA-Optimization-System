# Creating aws machine learning model
# This program uploads the finalData.csv file to S3, and used it as a data source to train a binary 
# classification model
import time,sys,random

import boto3

import S3

sys.path.append('./utils')
import aws
import base64
import json
import os
import sys

TIMESTAMP  =  time.strftime('%Y-%m-%d-%H-%M-%S')
S3_BUCKET_NAME = "mtadata_hhh"
S3_FILE_NAME = 'finalData.csv'
S3_URI = "s3://{0}/{1}".format(S3_BUCKET_NAME, S3_FILE_NAME)
DATA_SCHEMA = "temData.csv.schema"



# build model and then evaluate the model using testing data
def build_model(data_s3_url, schema_fn, recipe_fn, name, train_percent=70):     
    	ml = aws.getClient('machinelearning', 'us-east-1')                          
    	(train_ds_id, test_ds_id) = create_data_sources(ml, data_s3_url, schema_fn, 
                                                    train_percent, name)        
    	ml_model_id = create_model(ml, train_ds_id, recipe_fn, name)                
    	eval_id = create_evaluation(ml, ml_model_id, test_ds_id, name)              
                                                                                
    	return ml_model_id 

# create data sources (training data and testing data)
def create_data_sources(ml, data_s3_url, schema_fn, train_percent, name):       
    	train_ds_id = 'ds-' + base64.b32encode(os.urandom(10))                      
    	spec = {                                                                    
        	"DataLocationS3": data_s3_url,                                          
        	"DataRearrangement": json.dumps({                                       
            	"splitting": {                                                      
                	"percentBegin": 0,                                              
                	"percentEnd": train_percent                                     
            	}                                                                   
        	}),                                                                     
        	"DataSchema": open(schema_fn).read(),                                   
    	}                                                                           
    	ml.create_data_source_from_s3(                                              
        	DataSourceId=train_ds_id,                                               
        	DataSpec=spec,                                                          
        	DataSourceName=name + " - training split",                              
        	ComputeStatistics=True                                                  
    	)                                                                           
   	print("Created training data set %s" % train_ds_id)                         
                                                                                
    	test_ds_id = 'ds-' + base64.b32encode(os.urandom(10))                       
    	spec['DataRearrangement'] = json.dumps({                                    
        	"splitting": {                                                          
            	"percentBegin": train_percent,                                      
            	"percentEnd": 100                                                   
        	}                                                                       
    	})                                                                          
    	ml.create_data_source_from_s3(                                              
        	DataSourceId=test_ds_id,                                                
        	DataSpec=spec,                                                          
        	DataSourceName=name + " - testing split",                               
        	ComputeStatistics=True                                                  
    	)   
	print "Created test data set %s" % test_ds_id                              
    	return (train_ds_id, test_ds_id)                                            
                                                                                
# create ML model                                                                                
def create_model(ml, train_ds_id, recipe_fn, name):                             
    	model_id = 'ml-' + base64.b32encode(os.urandom(10))                         
    	ml.create_ml_model(                                                         
        	MLModelId=model_id,                                                     
        	MLModelName=name + " model",                                            
        	MLModelType="BINARY",  # we're predicting True/False values             
        	Parameters={                                                            
            	# Refer to the "Machine Learning Concepts" documentation            
            	# for guidelines on tuning your model                               
            	"sgd.maxPasses": "100",                                             
            	"sgd.maxMLModelSizeInBytes": "104857600",  # 100 MiB                
            	"sgd.l2RegularizationAmount": "1e-4",                               
        	},                                                                      
        	Recipe=open(recipe_fn).read(),                                          
        	TrainingDataSourceId=train_ds_id                                        
    	)                                                                           
    	print("Created ML Model %s" % model_id)                                     
    	return model_id                                                        

def create_evaluation(ml, model_id, test_ds_id, name):               
	eval_id = 'ev-' + base64.b32encode(os.urandom(10))               
    	ml.create_evaluation(                                            
        	EvaluationId=eval_id,                                        
        	EvaluationName=name + " evaluation",                         
        	MLModelId=model_id,                                          
        	EvaluationDataSourceId=test_ds_id                            
    	)                                                                
    	print("Created Evaluation %s" % eval_id)                         
    	return eval_id                                                   
                                                                     
                                                                     
if __name__ == "__main__":                                           
    	try:                                                             
        	data_s3_url = S3_URI                           
        	#schema_fn = "temData.csv.schema"                             
        	schema_fn = DATA_SCHEMA
		recipe_fn = "recipe.json"                                    
        	if len(sys.argv) > 2:                                        
            		name = sys.argv[1]                                       
        	else:                                                        
            		name = "Marketing sample"                                      
    	except:                                                                     
        	raise                                                        

    	newS3 = S3.S3(S3_FILE_NAME)
	newS3.S3_BUCKET_NAME = S3_BUCKET_NAME
	newS3.uploadData()
	print "upload success"
	
	model_id = build_model(data_s3_url, schema_fn, recipe_fn, name=name)
    	#print("""\nFor the next step in the demo, run:                             
    	#python use_model.py %s 0.77 s3://your-bucket/ml-output/""" % model_id) 
