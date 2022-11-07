import matplotlib.pyplot as plt
import numpy as np


def readFile(benchmarkTextFile,legend_name_1,legend_name_2,title,fig_name):
	"""
	Reads txt file for hadoop-spark benchmarking
	
	benchmarkTextFile: path to the text file that has execution times
	legend_name_1: name used for the legend for the first method
	legend_name_2: name used for the legend for the second method
	title: name used for the graph
	fig_name: name of figure to be saved as png
	"""
	benchmarkData = open(benchmarkTextFile, "r")
	
	# Read "real" execution time from file in arrays 
	hadoopTry1 = readData(benchmarkData)
	hadoopTry2 = readData(benchmarkData)
	hadoopTry3 = readData(benchmarkData)
	sparkTry1 = readData(benchmarkData)
	sparkTry2 = readData(benchmarkData)
	sparkTry3 = readData(benchmarkData)

	plotData([hadoopTry1,hadoopTry2,hadoopTry3],[sparkTry1,sparkTry2,sparkTry3],legend_name_1, legend_name_2, title, fig_name)
	
def readFileLinux(benchmarkTextFile,legend_name_1,legend_name_2,title,fig_name):
	"""
	Reads the executions time for hadoop vs linux. Since it is only one execution, we have to use a different function than readFile()
	
	benchmarkTextFile: path to the text file that has execution times
	legend_name_1: name used for the legend for the first method
	legend_name_2: name used for the legend for the second method
	title: name used for the graph
	fig_name: name of figure to be saved as png
	"""
	benchmarkData = open(benchmarkTextFile, "r")
	hadoop_time = 0
	linux_time = 0
	while (True):
		line = benchmarkData.readline()
		values = line.split("\t")
		if values[0] == "real":
			minutes = values[1].split("m")[0]
			seconds = values[1].split("m")[1].split("s")[0]
			hadoop_time = float(minutes * 60 + seconds)
			break
	while (True):
		line = benchmarkData.readline()
		values = line.split("\t")
		if values[0] == "real":
			minutes = values[1].split("m")[0]
			seconds = values[1].split("m")[1].split("s")[0]
			linux_time = float(minutes * 60 + seconds)
			break
	X = ['1st file']
	print("Hadoop took {}s".format(hadoop_time))
	print("Linux took {}s".format(linux_time))
	X_axis = np.arange(len(X))
	plt.bar(X_axis - 0.2, [hadoop_time], 0.4, label=legend_name_1)
	plt.bar(X_axis + 0.2, [linux_time], 0.4, label=legend_name_2)
	plt.xticks(X_axis,X)
	plt.ylabel("Time to execute (seconds)")
	plt.title(title)
	plt.legend()
	plt.savefig(fig_name)
	plt.clf()



def readData(benchmarkData):
	"""
	Reads data from real time for one execution of all 9 files.
	
	benchmarkTextFile: path to the text file that has execution times
	returns: array of real execution time for each file 
	"""

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
			i = i+1
	print(arr)
	return arr


def plotData(data_1_results,data_2_results,legend_name_1,legend_name_2,title,fig_name):
	"""
	Plots benchmark using matplotlib
	
	data_1_results: time results for all 3 executions on each file using first method
	data_2_results: time results for all 3 executions on each file using second method
	legend_name_1: name used for the legend for the first method
	legend_name_2: name used for the legend for the second method
	title: name used for the graph
	fig_name: name of figure to be saved as png
	"""
	
	# Compute average of all 3 executions
	data1Avg = [(data_1_results[0][i] + data_1_results[1][i] + data_1_results[2][i])/3 for i in range(9)]
	data2Avg = [(data_2_results[0][i] + data_2_results[1][i] + data_2_results[2][i])/3 for i in range(9)]
	
	
	X = ['1st file', '2nd file', '3rd file', '4th file', '5th file', '6th file', '7th file', '8th file', '9th file']
	X_axis = np.arange(len(X))
	plt.bar(X_axis - 0.2, data1Avg, 0.4, label=legend_name_1)
	plt.bar(X_axis + 0.2, data2Avg, 0.4, label=legend_name_2)
	plt.xticks(X_axis,X)
	plt.ylabel("Time to execute (seconds)")
	plt.title(title)
	plt.legend()
	plt.savefig(fig_name)
	plt.clf()

if __name__ == "__main__":
	readFile("benchmarking_time_results.txt", "hadoop","spark", "Average execution time for each test file (WordCount)", "Average_benchmark_hadoop_spark.png");
	readFileLinux("time_results.txt", "hadoop","linux", "Average execution time for each test file (WordCount)", "Average_benchmark_hadoop_linux.png")
