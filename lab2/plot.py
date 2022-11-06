import matplotlib.pyplot as plt
import numpy as np


def readFile(benchmarkTextFile):
	benchmarkData = open(benchmarkTextFile, "r")
	hadoopTry1 = readData(benchmarkData)
	hadoopTry2 = readData(benchmarkData)
	hadoopTry3 = readData(benchmarkData)
	sparkTry1 = readData(benchmarkData)
	sparkTry2 = readData(benchmarkData)
	sparkTry3 = readData(benchmarkData)

	plotData([hadoopTry1,hadoopTry2,hadoopTry3],[sparkTry1,sparkTry2,sparkTry3])
def readData(benchmarkData):
	arr = np.empty(9,dtype='d')
	i = 0
	while (i!=9):
		line = benchmarkData.readline()
		values = line.split("\t")
		if values[0] == "real":
			minutes = values[1].split("m")[0]
			seconds = values[1].split("m")[1].split("s")[0]
			arr[i] = minutes * 60 + seconds
			print(minutes)
			print(seconds)
			i+=1
	print(arr)
	return arr

def plotData(hadoopResults,sparkResults):
	hadoopAvg = [(hadoopResults[0][i] + hadoopResults[1][i] + hadoopResults[2][i])/3 for i in range(9)]
	sparkAvg = [(sparkResults[0][i] + sparkResults[1][i] + sparkResults[2][i])/3 for i in range(9)]
	print(hadoopAvg)
	print(sparkAvg)
	X = ['1st file', '2nd file', '3rd file', '4th file', '5th file', '6th file', '7th file', '8th file', '9th file']
	X_axis = np.arange(len(X))
	plt.bar(X_axis - 0.2, hadoopAvg, 0.4, label='hadoop')
	plt.bar(X_axis + 0.2, sparkAvg, 0.4, label='spark')
	plt.xticks(X_axis,X)
	plt.ylabel("Time to execute (seconds)")
	plt.title("Average execution time for each test file (WordCount)")
	plt.legend()
	plt.show()
	
readFile("benchmarking_time_results.txt");
