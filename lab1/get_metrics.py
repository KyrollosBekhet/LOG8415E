from datetime import datetime, timedelta
import boto3




client = boto3.client('cloudwatch', region_name='us-west-2')

response = client.get_metric_data(
    MetricDataQueries=[
        {

        }
    ],
    StartTime=datetime.utcnow()-timedelta(seconds=600), # Requests metrics from 10 minutes ago
    EndTime=datetime.utcnow(),
    LabelOptions={
        'Timezone': -0400
    }
)
