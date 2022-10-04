from datetime import datetime, timedelta
import boto3




client = boto3.client('cloudwatch', region_name='us-west-2')

response = client.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'cpu_usage'
            'MetricStat': {
                'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': 'CPUUtilization'          
                },
                'Period': 15,
                'Stat': 'Avg',
                'Unit': 'Percent'
            },
            'Period': 15, # Requests interval
        }
    ],
    StartTime=datetime.utcnow()-timedelta(seconds=600), # Requests metrics from 10 minutes ago
    EndTime=datetime.utcnow(),
    LabelOptions={
        'Timezone': -0400 # Timezone offset from UTC for Eastern Time
    }
)
