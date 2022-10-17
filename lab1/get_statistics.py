import boto3
import matplotlib.pyplot as plt
import numpy as np
from get_metrics import getMetric



def getStatistics(session):


    client = session.client('cloudwatch')

    # Get CPU Usage on instances
    repCPU = getMetric(client,'cpu_usage','AWS/EC2','CPUUtilization',30,'Sum','Percent',600)

    print(repCPU)
    

    #resp = repCPU['MetricDataResults'][0]


    #printPlot(resp)
    # Get request count on load balancer
    repREQCNT = getMetric(client, 'request_count', 'AWS/ApplicationELB', 'RequestCount', 60, 'Sum', 'Count', 600)
    print(repREQCNT)
    #resp = repREQCNT['MetricDataResults'][0]
    #printPlot(resp)

    # Get average target response time on load balancer 
    repTIME = getMetric(client, 'target_response_time', 'AWS/ApplicationELB','TargetResponseTime',60,'Average','Seconds',600)
    print(repTIME)

def printPlot(resp, fileName):

    y = np.array(resp['Values'][0])
    x = np.array(resp['Timestamp'][0])


    for n in range(1,len(resp['Values'])):

        y = np.append(x,resp['Values'][n])
        x = np.append(x,resp['Timestamp'][n])

    plt.scatter(x, y)
    plt.savefig(fileName)

