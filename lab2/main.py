import boto3
from instances import *
from security_group import *
import os
from ssh_connection import *

if __name__ == "__main__":
    session = boto3.Session(profile_name='default')
    ec2_client = session.client('ec2')
    ec2_resource = session.resource('ec2')

    vpcs = ec2_client.describe_vpcs()
    vpc_id = vpcs.get('Vpcs', [{}])[0].get('VpcId', '')

    instance_ami = 'ami-08c40ec9ead489470'
    #key_pair = ec2_client.describe_key_pairs()['KeyPairs'][0]
    key_pair = create_key_pair(ec2_client, "tp2Key")
    security_group_id = create_security_group(ec2_client, vpc_id)['GroupId']
    instance = None
    # TODO fix the chmod path
    commands = [
        "sudo apt-get update -y;",
        "sudo apt-get install git -y;",
        "git clone https://github.com/KyrollosBekhet/LOG8415E.git;",
        "chmod 777 install.sh;",
        "./install.sh;",
    ]
    try:
        instance = create_instances(ec2_resource, instance_ami, "m4.large",
                                    key_pair["KeyName"], "instance", 1, security_group_id)[0]
        instance.wait_until_running()
        print(instance.id)
        instance = ec2_resource.Instance(instance.id)
        print("instance is ready")
        public_ip = instance.public_ip_address
        print(public_ip)
        # TODO: Remove the file transfer since we will clone the git repository
        folder_path = os.path.curdir
        files = [
            os.path.join(folder_path, "install.sh"),
            os.path.join(folder_path, '4300.txt'),
        ]
        time.sleep(60)
        start_deployment(public_ip, files, commands, key_pair["KeyMaterial"])

    except Exception as e:
        print(e)

    finally:
        if instance is not None:
            instance.terminate()
            instance.wait_until_terminated()

        ec2_client.delete_key_pair(KeyName="tp2Key")
        delete_security_group(ec2_client, security_group_id)

