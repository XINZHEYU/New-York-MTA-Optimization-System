# Creating aws machine learning model
# This program uploads the finalData.csv file to S3, and used it as a data sourc
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

newS3 = S3.S3(S3_FILE_NAME)
newS3.S3_BUCKET_NAME = S3_BUCKET_NAME
newS3.uploadData()
print "upload success"
