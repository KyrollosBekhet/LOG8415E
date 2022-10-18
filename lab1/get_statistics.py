import boto3
import matplotlib.pyplot as plt
import numpy as np
from get_metrics import getMetric, getMetricInstance


# Get all cloudwatch statistics
#   instance_ids: array containing all instance ids
#   session: session of boto3
def getStatistics(session,instance_ids):

    print(instance_ids)
    
    client = session.client('cloudwatch')

    try:
        # Get CPU Usage on instances
        repCPU = getMetricInstance(client, instance_ids,'cpu_usage','AWS/EC2','CPUUtilization',30,'Sum','Percent',600)
        print(repCPU)
        printPlot(repCPU, "cpu_utilization.png","CPU Utilization")
    except Exception as e:
        print(e)
        
    try:
        # Get Network In on instances
        repNetIn = getMetricInstance(client, instance_ids,'network_in','AWS/EC2','NetworkIn',30,'Sum','Bytes',600)
        print(repNetIn)
        printPlot(repNetIn, "network_in.png","NetworkIn")
    except Exception as e:
        print(e)
    try:
        # Get Network Out on instances
        repNetOut = getMetricInstance(client, instance_ids,'network_out','AWS/EC2','NetworkOut',30,'Sum','Bytes',600)
        print(repNetOut)
        printPlot(repNetOut, "network_out.png","NetworkOut")
    except Exception as e:
        print(e)
    
    repREQCNT = getMetric(client, 'request_count', 'AWS/ApplicationELB', 'RequestCount', 60, 'Sum', 'Count', 600, session)
    print(repREQCNT)
    # Get average target response time on load balancer 
    repTIME = getMetric(client, 'target_response_time', 'AWS/ApplicationELB','TargetResponseTime',60,'Average','Seconds',600, session)
    print(repTIME)
    
    
# Prints the plot
#   resp: the response dictionnary 
#   fileName: the file name to be used
#   ylabel: the label to be used on the y axis
def printPlot(resp, fileName, ylabel):

    y = np.array(resp['MetricDataResults'][0]['Values'])
    x = np.array(resp['MetricDataResults'][0]['Timestamps'])

    plt.plot(x, y, label=resp['MetricDataResults'][0]['Label'])
    
    for r in range(1,len(resp['MetricDataResults'])):
        x1 = np.array(resp['MetricDataResults'][r]['Timestamps'])
        y1 = np.array(resp['MetricDataResults'][r]['Values'])
        plt.plot(x1,y1,label=resp['MetricDataResults'][r]['Label'])
        print(y1)
    # Labels for both axis
    plt.xlabel("Timestamp")
    plt.ylabel(ylabel)
    plt.legend(loc="upper left")
    # Save as png image
    plt.savefig(fileName)
    # Clear the plot for future use
    plt.clf()

