import time,csv,sys
from pytz import timezone
from datetime import datetime

sys.path.append('/home/root/Lab3/assignment/e6765_spring16/utils')
import mtaUpdates
import tripupdate, vehicle, alert, mtaUpdates, aws
import aws
import calendar
import sys
# This script should be run seperately before we start using the application
# Purpose of this script is to gather enough data to build a training model for Amazon machine learning
# Each time you run the script it gathers data from the feed and writes to a file
# You can specify how many iterations you want the code to run. Default is 50
# This program only collects data. Sometimes you get multiple entries for the same tripId. we can timestamp the 
# entry so that when we clean up data we use the latest entry

# Change DAY to the day given in the feed
DAY = datetime.today().strftime("%A")
TIMEZONE = timezone('America/New_York')

global ITERATIONS

#Default number of iterations
ITERATIONS = int(sys.argv[1])


#################################################################
####### Note you MAY add more datafields if you see fit #########
#################################################################

# column headers for the csv file
columns =['timestamp','tripId','route','day','timeToReachExpressStation','timeToReachDestination']
def conv_route(routeId):
	if routeId == '1':
		return 'Local'
	if routeId == '2' or routeId == '3':
		return 'Express'
	return -1

# convert unix timestamp to minutes past midnight 
def conv_time(unixtime):
	normal = datetime.fromtimestamp(unixtime)
	h = normal.hour
	m = normal.minute
	total = h*60 + m
	return total

def matchdata(headers, tripUpdate, alerts, vehicle, timestamp):
	row = []
	str120 = unicode('120S')
	str127 = unicode('127S')
	tup = ()
	for item in tripUpdate:
		flag = 0
		for v in vehicle:
			if v.tripId == item.tripId and v.routeId == item.routeId:
				flag = 1 
				if conv_route(item.routeId) != -1:
					# print TIMEZONE
					# print 'timestamp type:', type(timestamp)
					new_time = conv_time(timestamp)
					if v.currentStopId == str120 and item.futureStops.has_key(str127):
						tup = (new_time, item.tripId, conv_route(item.routeId), DAY, conv_time(v.timestamp), conv_time(item.futureStops[str127][0]))
						row.append(tup)
					elif v.currentStopId == str127 and item.futureStops.has_key(str120) :
						tup = (new_time, item.tripId, conv_route(item.routeId), DAY, conv_time(item.futureStops[str120][0]), conv_time(v.timestamp))
						row.append(tup)
					elif item.futureStops.has_key(str120) and item.futureStops.has_key(str127):
						tup = (new_time, item.tripId, conv_route(item.routeId), DAY, conv_time(item.futureStops[str120][0]), conv_time(item.futureStops[str127][0]))
						row.append(tup)
		if not flag:
			if conv_route(item.routeId) != -1:
				if item.futureStops.has_key(str120) and item.futureStops.has_key(str127):
					tup = (conv_time(timestamp), item.tripId, conv_route(item.routeId), DAY, conv_time(item.futureStops[str120][0]), conv_time(item.futureStops[str127][0]))
					row.append(tup)
	return row





def main(fileName):
    # API key
    with open('../../config.txt', 'rb') as keyfile:
        APIKEY = keyfile.read().rstrip('\n')
        keyfile.close()

	### INSERT YOUR CODE HERE ###
	Dynamodb_table_name = "mataData"
	dynamodb = aws.getResource('dynamodb', 'us-east-1')
	table = dynamodb.Table('mtaData')
	f = open(fileName, 'a')
	f_csv = csv.writer(f)
	# f_csv.writerow(columns)	
	for i in range(ITERATIONS):
		data = mtaUpdates.mtaUpdates("")
	

		tripUpdate, alerts, vehicle, timestamp = data.getTripUpdates()
	
		#headers = ['Timestamp', 'tripId', 'Route', 'Day of the week', 'Time at which it reaches express station', 'Time at which it reaches the destination']
		#f = open(fileName, 'a')
		#f_csv = csv.writer(f)
		row = matchdata(columns, tripUpdate, alerts, vehicle, timestamp)
		#print row
		f_csv.writerows(row)
		#f.close()	
		print "file write success iter:", i
	f.close()

if __name__ == "__main__":
	main('cgl.csv')

