## This program is used to clean out the data from the csv that you collected.
## It aims at removing duplicate entries and extracting any further insights 
## that the author(s) of the code may see fit

## Usage (for file as is currently): python buildTrainingDataSet.py <filename of file from part 1>
  
import sys

# Pandas is a python library used for data analysis
import pandas
from pandas import read_csv
from pytz import timezone
from datetime import datetime
#import numpy as np

TIMEZONE = timezone('America/New_York')



def main(fileHandle):
	# This creates a dataframe
	rawData = read_csv(fileHandle)

	# Remove duplicate entries based on tripId, retain the one with maximum timestamp
	data  =rawData.groupby('tripId').apply(lambda x: x.ix[x.timestamp.idxmax()])

	# Seperate all the local trains and form a new data frame
	localTrains = data[data.route == 'Local']

	# Add a label column to local trains to decide whether to change to express train
	localTrains['Label'] = 0
	#print localTrains

	# Express trains
	expressTrains = data[data.route == 'Express']	
	
	#expressTrains.sort(columns='timeToReachExpressStation', ascending=True)
	#expressTrains.sort_values('timeToReachExpressStation', ascending=True)	

	e_len = len(expressTrains)
	l_len = len(localTrains)
	
	"""# Clean the data whose timestamp is greater than timetoreachexpress station 
	for i in range(e_len):
		if (expressTrains.ix[i, 'timestamp'] > expressTrains.ix[i, 'timeToReachExpressStation'] ):
			print expressTrains.ix[i, 'timestamp'], expressTrains.ix[i, 'timeToReachExpressStation']
			expressTrains.drop(expressTrains.ix[i, 'tripId'])
	"""
	for i in range(l_len):
		etime_local = localTrains.ix[i,'timeToReachExpressStation']	# Time to reach 96st for local train
		dtime_local = localTrains.ix[i,'timeToReachDestination']	# Time to reach 42st for local train
		first = -1	# First express train to reach 96st
		for j in range(e_len):
			tmp_time = expressTrains.ix[j,'timeToReachExpressStation']
			if tmp_time >= etime_local:
				first = j
				break
		dtime_express = expressTrains.ix[first,'timeToReachExpressStation']
		if dtime_express < dtime_local:
			localTrains.ix[i,'Label'] = 1
			
				
		
	#print localTrains.ix[0]
	#print localTrains.ix[0]['timestamp']
	#print localTrains


	# Find combinations:
	
	# 1. Find the time difference (to reach 96th) between all combinations of local trains and express
	# 2. Consider only positive delta
	# 3. Make the final table
	# Create a new data frame for final table
	
	finalData = pandas.DataFrame(localTrains)

	

	finalData.to_csv("finalData.csv",index=False)



if __name__ == "__main__":

	lengthArg = len(sys.argv)


	if lengthArg < 2:
		print "Missing arguments"
		sys.exit(-1)

	if lengthArg > 2:
		print "Extra arguments"
		sys.exit(-1)
	
	fileHandle = sys.argv[1]
	main(fileHandle)
