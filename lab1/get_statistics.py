import boto3
import matplotlib.pyplot as plt
import numpy as np
from get_metrics.py import getMetric



client = boto3.client('cloudwatch', region_name='us-east-2')

# Wait some time

# Get CPU Usage on instances
repCPU = getMetric(client,'cpu_usage','AWS/EC2','CPUUtilization',15,'Sum','Percent',600)

print(repCPU['Messages'])


resp = repCPU['MetricDataResults'][0]


printPlot(resp)
# Get request count on load balancer
repREQCNT = getMetric(client, 'request_count', 'AWS/ApplicationELB', 'RequestCount', 15, 'Sum', 'Count', 600)

# Get average target response time on load balancer 
repTIME = getMetric(client, 'target_response_time', 'AWS/ApplicationELB','TargetResponseTime',15,'Average','Seconds',600)

def printPlot(resp):

y = np.array(resp['Values'][0])
x = np.array(resp['Timestamp'][0])


for n in range(1,len(resp['Values'])):

    y = np.append(x,resp['Values'][n])
    x = np.append(x,resp['Timestamp'][n])

plt.scatter(x, y)
plt.show()

