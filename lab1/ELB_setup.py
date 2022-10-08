def create_load_balancer(client, subnets, security_groups, target_groups):
    """

    :param client: The client connection using boto3
    :param subnets: The subnets for request mapping
    :param security_groups: The security groups ids that allow the traffic
    :param target_groups: The ARN of the target groups
    :return: The load balancer information after the creation
    Response syntax:
        {
            LoadBalancerArn: 'string',
            LoadBalancerDNS: 'string',
            ListenerArn: 'string',
            RuleArns: [first_rule_response: String[]
        },
    """

    # create the load balancer to serve the subnets and with the security groups created
    load_balancer_creation_response = client.create_load_balancer(Name="my-load-balancer",
                                                                  Subnets=subnets,
                                                                  SecurityGroups=security_groups,
                                                                  Scheme='internet-facing',
                                                                  Type='application', IpAddressType='ipv4')
    load_balancer = load_balancer_creation_response['LoadBalancers'][0]

    # add listener
    listener_response = client.create_listener(LoadBalancerArn=load_balancer['LoadBalancerArn'], Port=80,
                                               DefaultActions=[
                                                   {
                                                       'TargetGroupArn': target_groups[0],
                                                       'Type': "forward",
                                                   },
                                               ],
                                               Protocol='HTTP')
    listener = listener_response['Listeners'][0]
    # create rules to specify the request paths if /cluster1 forward target group 1
    # I want to forward the requests not to redirect
    first_rule_response = client.create_rule(ListenerArn=listener["ListenerArn"],
                                             Actions=[
                                                 {
                                                     'TargetGroupArn': target_groups[0],
                                                     'Type': "forward",
                                                 },
                                             ],
                                             Conditions=[
                                                 {
                                                     'Field': 'path-pattern',
                                                     'Values': [
                                                         '/cluster1'
                                                     ],
                                                 },
                                             ],
                                             Priority=20)["Rules"][0]

    second_rule_response = client.create_rule(ListenerArn=listener["ListenerArn"],
                                              Actions=[
                                                  {
                                                      'TargetGroupArn': target_groups[1],
                                                      'Type': "forward",
                                                  },
                                              ],
                                              Conditions=[
                                                  {
                                                      'Field': 'path-pattern',
                                                      'Values': [
                                                          '/cluster2'
                                                      ],
                                                  },
                                              ],
                                              Priority=15)['Rules'][0]
    ret = {
        'LoadBalancerArn': load_balancer['LoadBalancerArn'],
        'LoadBalancerDNS': load_balancer['DNSName'],
        'ListenerArn': listener["ListenerArn"],
        'RuleArns': [first_rule_response['RuleArn'], second_rule_response['RuleArn']]
    }
    return ret


def create_target_groups(client, name, vpc_id):
    """

    :param vpc_id: a string representing the virtual private cloud id
    :param client: The client connection using boto3
    :param name: the name of the cluster or target group
    :return: the newly created target group
    Response syntax:
        {
    'TargetGroups': [
        {
            'TargetGroupArn': 'string',
            'TargetGroupName': 'string',
            'Protocol': 'HTTP'|'HTTPS'|'TCP'|'TLS'|'UDP'|'TCP_UDP'|'GENEVE',
            'Port': 123,
            'VpcId': 'string',
            'HealthCheckProtocol': 'HTTP'|'HTTPS'|'TCP'|'TLS'|'UDP'|'TCP_UDP'|'GENEVE',
            'HealthCheckPort': 'string',
            'HealthCheckEnabled': True|False,
            'HealthCheckIntervalSeconds': 123,
            'HealthCheckTimeoutSeconds': 123,
            'HealthyThresholdCount': 123,
            'UnhealthyThresholdCount': 123,
            'HealthCheckPath': 'string',
            'Matcher': {
                'HttpCode': 'string',
                'GrpcCode': 'string'
            },
            'LoadBalancerArns': [
                'string',
            ],
            'TargetType': 'instance'|'ip'|'lambda'|'alb',
            'ProtocolVersion': 'string',
            'IpAddressType': 'ipv4'|'ipv6'
        },
    ]
    }
    """
    return client.create_target_group(Name=name, Protocol="HTTP", Port=80, VpcId=vpc_id)


def add_instance_to_target_group(elb_client, cluster_arn, instances_id):
    elb_client.register_targets(
        TargetGroupArn=cluster_arn,
        Targets=instances_id
    )
