def delete_target_group(client, target_group_arn):
    """

    :param client: The client connection using boto3
    :param target_group_arn: the resource name of the target group
    :return: 0
    """
    client.delete_target_group(TargetGroupArn=target_group_arn)


def delete_load_balancer(client, load_balancer_arn):
    """

    :param client: The elb client connection using boto3
    :param load_balancer_arn: the resource name of the load balancer to be deleted
    :return: 0
    """
    client.delete_load_balancer(LoadBalancerArn=load_balancer_arn)
