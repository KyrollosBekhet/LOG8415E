from ELB_setup import *


""" 
TODO: Remove the main function the goal of this method is to test the creation of the load balancer
 and target groups. Also to identify what is needed to create the load balancer
"""


def main():
    cluster1 = create_target_groups("cluster1")["TargetGroups"][0]
    cluster2 = create_target_groups("cluster2")["TargetGroups"][0]
    target_groups = [cluster1['TargetGroupArn'], cluster2['TargetGroupArn']]
    # Hardcoded security group id
    subnets = ['subnet-0368628d6c8694be6', 'subnet-0584deae6391f04bf']
    security_groups = ['sg-03d6e26eae0579bd9']
    create_load_balancer(subnets, security_groups, target_groups)


main()
