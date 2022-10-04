import boto3


def create_key_pair(ec2_resource,
                    key_name):
    """
    Creates a key pair to securely connect to the AWS instances
    :param key_name: The name of the key pair
    :param ec2_resource: The ec2 resource which will create the key pair
    :return: The newly created key_pair
    """
    return ec2_resource.create_key_pair(KeyName=key_name)


def create_instances(ec2_resource, image_id, instance_type, key_name, tags,
                     subnet_id, vpc_id, count,
                     security_group_name="TP1automaticSG"):
    instance_params = {
        'ImageId': image_id, 'InstanceType': instance_type,
        'KeyName': key_name, 'SecurityGroups': security_group_name,
        'SubnetId': subnet_id, 'VpcId': vpc_id, 'tags': tags
    }
    instances = ec2_resource.create_instances(**instance_params, MinCount=count, MaxCount=count)
    print(instances)
