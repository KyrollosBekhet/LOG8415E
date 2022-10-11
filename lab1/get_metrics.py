from datetime import datetime, timedelta
import boto3




client = boto3.client('cloudwatch', region_name='us-west-2')



def getCpuUsage(client, period, time):

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'cpu_usage'
                'MetricStat': {
                    'Metric': {
                            'Namespace': 'AWS/EC2',
                            'MetricName': 'CPUUtilization'          
                    },
                    'Period': period,
                    'Stat': 'Avg',
                    'Unit': 'Percent'
                },
                'Period': period, # Requests interval
            }
        ],
        StartTime=datetime.utcnow()-timedelta(seconds=time), # Requests metrics from 10 minutes ago
        EndTime=datetime.utcnow(),
        LabelOptions={
            'Timezone': -0400 # Timezone offset from UTC for Eastern Time
        }
    )
