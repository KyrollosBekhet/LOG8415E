import boto3


def clean_up():
    # Creating session using default credentials and configuration.
    session = boto3.Session(profile_name='default')

    elb_client = session.client('elbv2')
    ec2_client = session.client('ec2')
    ec2_resource = session.resource('ec2')
