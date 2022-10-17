import boto3
import matplotlib.pyplot as plt
import numpy as np
from get_metrics import getMetric, getMetricInstance



def getStatistics(session,instance_ids):

    print(instance_ids)
    
    client = session.client('cloudwatch')

    # Get CPU Usage on instances
    
    try:
        repCPU = getMetricInstance(client, instance_ids,'cpu_usage','AWS/EC2','CPUUtilization',30,'Sum','Percent',600)
        print(repCPU)
        printPlot(repCPU, "cpu_utilization.png","CPU Utilization")
    except Exception as e:
        print(e)
        
    try:
        repNetIn = getMetricInstance(client, instance_ids,'network_in','AWS/EC2','NetworkIn',30,'Sum','Bytes',600)
        print(repNetIn)
        printPlot(repNetIn, "network_in.png","NetworkIn")
    except Exception as e:
        print(e)
    try:
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

def printPlot(resp, fileName, ylabel):

    y = np.array(resp['MetricDataResults'][0]['Values'])
    x = np.array(resp['MetricDataResults'][0]['Timestamps'])
    #print(x)
    #print(y)
    #print(x.shape)
    #print(y.shape)
    #for n in range(1,len(resp['Values'])):

    #    y = np.append(x,resp['Values'][n])
    #    x = np.append(x,resp['Timestamp'][n])

    plt.plot(x, y)
    
    for r in range(1,len(resp['MetricDataResults'])):
        x1 = np.array(resp['MetricDataResults'][r]['Timestamps'])
        y1 = np.array(resp['MetricDataResults'][r]['Values'])
        plt.plot(x1,y1)
        print(y1)
    plt.xlabel("Timestamp")
    plt.ylabel(ylabel)
        
    plt.savefig(fileName)
    plt.clf()

