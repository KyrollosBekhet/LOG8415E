import traceback
from curses import keyname
from instances import *
from ssh_connection import *
from security_group import *
import boto3
from io import StringIO


def run():
    session = boto3.Session(profile_name='default')
    ec2_client = session.client('ec2')
    ec2_resource = session.resource('ec2')

    vpcs = ec2_client.describe_vpcs()
    vpc_id = vpcs.get('Vpcs', [{}])[0].get('VpcId', '')
    sg = create_security_group(ec2_client, vpc_id)
    sn_all = ec2_client.describe_subnets()
    subnets = []
    for sn in sn_all['Subnets']:
        if sn['AvailabilityZone'] == 'us-east-1a' or \
                sn['AvailabilityZone'] == 'us-east-1b':
            subnets.append(sn['SubnetId'])

    response = create_key_pair(ec2_client, "key_pair")
    print(response)
    instance_ami = 'ami-08c40ec9ead489470'
    create_instances(ec2_resource, instance_ami, "t2.micro",
                     "key_pair", "instance", subnets[0], 1, sg['GroupId'])

    awake = False
    # for now number of instances are 1
    awake_instances = None
    while awake is False:
        # Name filter used to prevent existing instances from interfering
        awake_instances = ec2_resource.instances.filter(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Name', 'Values': ['instance']}
            ]
        )
        if len(list(awake_instances.all())) == 1:
            awake = True

    public_ips = [instance.public_ip_address for instance in awake_instances.all()]

    commands = [
        "echo hi",
        "mkdir folder"
        "ls",
        "whoami"
    ]

    time.sleep(30)
    try:
        for ip in public_ips:
            ssh_username = "ubuntu"
            ssh_key_file = StringIO(response["KeyMaterial"])
            ssh_connection = paramiko.SSHClient()
            rsa_key = paramiko.RSAKey.from_private_key(ssh_key_file)
            ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_connection.connect(hostname=ip, username=ssh_username,
                                   pkey=rsa_key, allow_agent=False, look_for_keys=False)
            print("connection success")
            for command in commands:
                print("running command: {}".format(command))
                _, stdout, stderr = ssh_connection.exec_command(command)
                print(stdout.read())
                print(stderr.read())

    except Exception as ex:
        traceback.print_exc()

    finally:
        time.sleep(5)
        ids = []
        for ins in awake_instances.all():
            ids.append({"Id": ins.id})

        terminate_instances(ec2_resource, ids)
        ec2_client.delete_key_pair(KeyName="key_pair")
        delete_security_group(ec2_client, sg['GroupId'])


if __name__ == "__main__":
    run()
