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
def getMetric(client, metric_id, namespace, metric_name, period, stat, unit, time):

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': metric_id,
                'MetricStat': {
                    'Metric': {
                            'Namespace': namespace,
                            'MetricName': metric_name ,       
                    },
                    'Period': period,
                    'Stat': stat,
                    'Unit': unit,
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
    
