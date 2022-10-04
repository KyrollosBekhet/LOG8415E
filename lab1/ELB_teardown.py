def delete_target_group(client, target_group_arn):
    """

    :param client: The client connection using boto3
    :param target_group_arn: the resource name of the target group
    :return: 0
    """
    client.delete_target_group(TargetGroupArn=target_group_arn)


def delete_load_balancer(client, load_balancer):
    """

    :param client: The elb client connection using boto3
    :param load_balancer: the dict that has all the resource names
    :return: 0
    """
    for rule_arn in load_balancer['RuleArns']:
        client.delete_rule(RuleArn=rule_arn)

    client.delete_listener(ListenerArn=load_balancer['ListenerArn'])
    client.delete_load_balancer(LoadBalancerArn=load_balancer['LoadBalancerArn'])
