import boto3

ec2 = boto3.resource('ec2')


def create_security_group(ec2):
    sG = ec2.create_security_group(
        Description="security group TP1",
        GroupName="TP1automaticSG"
    )
    add_outbound_rules(sG)
    add_inbound_rules(sG)


def add_inbound_rules(security_group):
    # ingress_rules
    ip_permission = [{
        'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
        {
            'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }]
    security_group.authorize_ingress(IpPermissions=ip_permission)


def add_outbound_rules(security_group):
    # egress_rules
    ip_permission = [{
        'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }, {
        'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }]

    security_group.authorize_egress(IpPermissions=ip_permission)


if __name__ == "__main__":
    create_security_group(ec2)
