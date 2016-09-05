import csv
f = open('finalData.csv', 'r')
ff = open('final.csv', 'a+')
f_csv = csv.reader(f)
ff_csv = csv.writer(ff)
i = 1

for row in f_csv:
	if i % 8 == 7:
		#print row
		ff_csv.writerow(row)
	i = i+1

f.close()
ff.close()

