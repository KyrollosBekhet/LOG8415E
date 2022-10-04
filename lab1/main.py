import time

from ELB_setup import *
import boto3
from ELB_teardown import *

""" 
TODO: Remove the main function the goal of this method is to test the creation of the load balancer
 and target groups. Also to identify what is needed to create the load balancer
"""


def main():
    client = boto3.client('elbv2')
    vpc_id = ' '
    cluster1 = create_target_groups(client, "cluster1", vpc_id)["TargetGroups"][0]
    cluster2 = create_target_groups(client, "cluster2", vpc_id)["TargetGroups"][0]
    target_groups = [cluster1['TargetGroupArn'], cluster2['TargetGroupArn']]
    # Hardcoded security group id
    subnets = ['subnet-0368628d6c8694be6', 'subnet-0584deae6391f04bf']
    security_groups = ['sg-03d6e26eae0579bd9']
    load_balancer = create_load_balancer(subnets, security_groups, target_groups)
    # wait 30 seconds to simulate an interruption
    time.sleep(30)
    # Tear down
    for target_group in target_groups:
        delete_target_group(target_group)

    delete_load_balancer(load_balancer['LoadBalancerArn'])


main()
