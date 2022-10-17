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
        printPlot(repCPU, "test","CPU Utilization")
    except Exception as e:
        print(e)
    #resp = repCPU['MetricDataResults'][0]


    #printPlot(resp)
    # Get request count on load balancer
    
    #resp = repREQCNT['MetricDataResults'][0]
    #printPlot(resp)
    repREQCNT = getMetric(client, 'request_count', 'AWS/ApplicationELB', 'RequestCount', 60, 'Sum', 'Count', 600)
    print(repREQCNT)
    # Get average target response time on load balancer 
    repTIME = getMetric(client, 'target_response_time', 'AWS/ApplicationELB','TargetResponseTime',60,'Average','Seconds',600)
    print(repTIME)

def printPlot(resp, fileName, ylabel):

    y = np.array(resp['MetricDataResults'][0]['Values'])
    x = np.array(resp['MetricDataResults'][0]['Timestamp'])


    #for n in range(1,len(resp['Values'])):

    #    y = np.append(x,resp['Values'][n])
    #    x = np.append(x,resp['Timestamp'][n])

    plt.scatter(x, y)
    
    for r in range(1,resp['MetricDataResults']):
        y1 = np.array(resp['MetricDataResults'][r]['Values'])
        plt.scatter(x,y1)
        
    plt.xlabel("Timestamp")
    plt.ylabel(ylabel)
        
    plt.savefig(fileName)

