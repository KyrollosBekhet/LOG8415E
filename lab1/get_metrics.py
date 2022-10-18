from datetime import datetime, timedelta
import boto3


# getMetric: get a specific CloudWatch metric.
#
#   client: The CloudWatch client
#   metric_id: The metric id, to be used in graphics
#   namespace: The namespace where the metric is
#   metric_name: The name of the metric
#   period: Period between each data point, in seconds
#   stat: The stat used for the metric (SampleCount, Average, Sum, Minimum, Maximum)
#   unit: The unit used for the metric (Percent, Seconds, Count, etc.)
#   time: The delta between now and the start time of the metric recording (seconds) 
#
def getMetric(client, metric_id, namespace, metric_name, period, stat, unit, time, session):
    
    
    resp = session.client('elbv2').describe_target_groups()
    print(resp['TargetGroups'][0]['LoadBalancerArns'][0])

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': metric_id,
                'MetricStat': {
                    'Metric': {
                            'Namespace': namespace,
                            'MetricName': metric_name ,
                            'Dimensions': [ 
                                {
                                    "Name":"LoadBalancer",
                                    "Value":resp['TargetGroups'][0]['LoadBalancerArns'][0],
                                                            
                                },
                                {
                                    "Name":"TargetGroup",
                                    "Value":resp['TargetGroups'][0]['TargetGroupArn'],
                            
                                }]      
                    },
                    'Period': period,
                    'Stat': stat,
                    #'Unit': unit,
                }
            },
            {
                'Id': "metric_id",
                'MetricStat': {
                    'Metric': {
                            'Namespace': namespace,
                            'MetricName': metric_name ,
                            'Dimensions': [ 
                                {
                                    "Name":"LoadBalancer",
                                    "Value":resp['TargetGroups'][1]['LoadBalancerArns'][0],
                                                            
                                },
                                {
                                    "Name":"TargetGroup",
                                    "Value":resp['TargetGroups'][1]['TargetGroupArn'],
                            
                                }]      
                    },
                    'Period': period,
                    'Stat': stat,
                    #'Unit': unit,
                }
            }
        ],
        StartTime=datetime.utcnow()-timedelta(seconds=time), # Requests metrics from 10 minutes ago
        EndTime=datetime.utcnow(),
        LabelOptions={
            'Timezone': '-0400' # Timezone offset from UTC for Eastern Time
        }
    )
    
    return response
    
    
# getMetric: get a specific CloudWatch instance metric.
#
#   client: The CloudWatch client
#   instance_ids: Array containing each instance ids
#   metric_id: The metric id, to be used in graphics
#   namespace: The namespace where the metric is
#   metric_name: The name of the metric
#   period: Period between each data point, in seconds
#   stat: The stat used for the metric (SampleCount, Average, Sum, Minimum, Maximum)
#   unit: The unit used for the metric (Percent, Seconds, Count, etc.)
#   time: The delta between now and the start time of the metric recording (seconds)

def getMetricInstance(client, instance_ids, metric_id, namespace, metric_name, period, stat, unit, time):

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': metric_id,
                'MetricStat': {
                    'Metric': {
                            'Namespace': namespace,
                            'MetricName': metric_name,
                            'Dimensions': [ 
                                {
                                    "Name":"InstanceId",
                                    "Value":instance_ids[0],
                            
                                }]       
                    },
                    'Period': period,
                    'Stat': stat,
                    'Unit': unit,
                }
            },
            {
                'Id': "metric_id2",
                'MetricStat': {
                    'Metric': {
                            'Namespace': namespace,
                            'MetricName': metric_name,
                            'Dimensions': [ 
                                {
                                    "Name":"InstanceId",
                                    "Value":instance_ids[1],
                            
                                }]       
                    },
                    'Period': period,
                    'Stat': stat,
                    'Unit': unit,
                }
            },
            {
                'Id': "metric_id3",
                'MetricStat': {
                    'Metric': {
                            'Namespace': namespace,
                            'MetricName': metric_name,
                            'Dimensions': [ 
                                {
                                    "Name":"InstanceId",
                                    "Value":instance_ids[2],
                            
                                }]       
                    },
                    'Period': period,
                    'Stat': stat,
                    'Unit': unit,
                }
            },
            {
                'Id': "metric_id4",
                'MetricStat': {
                    'Metric': {
                            'Namespace': namespace,
                            'MetricName': metric_name,
                            'Dimensions': [ 
                                {
                                    "Name":"InstanceId",
                                    "Value":instance_ids[3],
                            
                                }]       
                    },
                    'Period': period,
                    'Stat': stat,
                    'Unit': unit,
                }
            },
        ],
        StartTime=datetime.utcnow()-timedelta(seconds=time), # Requests metrics from 10 minutes ago
        EndTime=datetime.utcnow(),
        LabelOptions={
            'Timezone': '-0400' # Timezone offset from UTC for Eastern Time
        }
    )
    
    return response
    
