import time

from ELB_setup import *
import boto3
from ELB_teardown import *
from security_group import *
from instances import *

""" 
TODO: Remove the main function the goal of this method is to test the creation of the load balancer
 and target groups. Also to identify what is needed to create the load balancer
"""


def main():
    elb_client = boto3.client('elbv2')
    ec2_client = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')
    default_security_group = ec2_client.describe_security_groups(GroupNames=['default'])['SecurityGroups'][0]
    vpcs = ec2_client.describe_vpcs()
    vpc_id = vpcs.get('Vpcs', [{}])[0].get('VpcId', '')
    sg = create_security_group(ec2_client, vpc_id)
    cluster1 = create_target_groups(elb_client, "cluster1", vpc_id)["TargetGroups"][0]
    cluster2 = create_target_groups(elb_client, "cluster2", vpc_id)["TargetGroups"][0]
    target_groups = [cluster1['TargetGroupArn'], cluster2['TargetGroupArn']]

    sn_all = ec2_client.describe_subnets()
    subnets = []
    for sn in sn_all['Subnets']:
        if sn['AvailabilityZone'] == 'us-east-1a' or sn['AvailabilityZone'] == 'us-east-1b':
            print(sn)
            subnets.append(sn['SubnetId'])

    key_name = "private_automatic_key"
    instances_ami = 'ami-08c40ec9ead489470'

    private_key = ec2_client.describe_key_pairs()['KeyPairs'][0]
    try:
        create_instances(ec2_resource, instances_ami, "t2.micro",
                         private_key["KeyName"], "cluster1", subnets[1], vpc_id, 1
                         , sg['GroupId'])
        print("Instance created")

        instances = ec2_resource.instances
        for instance in instances:
            print(instance.id, instance.tags)
    except Exception as e:
        print(e)

    security_groups = [sg['GroupId']]
    load_balancer = create_load_balancer(elb_client, subnets,
                                         security_groups, target_groups)
    print("Set up completed")
    # wait 30 seconds to simulate an interruption
    time.sleep(5)
    # Tear down
    delete_load_balancer(elb_client, load_balancer)
    for target_group in target_groups:
        delete_target_group(elb_client, target_group)

    time.sleep(5)
    #delete_security_group(ec2_client, sg['GroupId'])
    print("Successfully deleted")


main()
