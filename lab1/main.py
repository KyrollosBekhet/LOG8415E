from ELB_setup import *
from ELB_teardown import *
from endpoint_call import *
from instances import *
from ipaddress import ip_address
from nginx_file_writter import *
from security_group import *
from ssh_connection import *
from threading import Thread

import boto3
import time
from get_statistics import getStatistics


if __name__ == '__main__':
    # Creating session using default credentials and configuration.
    session = boto3.Session(profile_name='default')

    elb_client = session.client('elbv2')
    ec2_client = session.client('ec2')
    ec2_resource = session.resource('ec2')

    vpcs = ec2_client.describe_vpcs()
    vpc_id = vpcs.get('Vpcs', [{}])[0].get('VpcId', '')

    sg = create_security_group(ec2_client, vpc_id)

    cluster1 = create_target_groups(elb_client, "cluster1", vpc_id)["TargetGroups"][0]
    cluster2 = create_target_groups(elb_client, "cluster2", vpc_id)["TargetGroups"][0]

    target_groups = [cluster1['TargetGroupArn'], cluster2['TargetGroupArn']]

    security_groups = [sg['GroupId']]

    sn_all = ec2_client.describe_subnets()
    subnets = []
    for sn in sn_all['Subnets']:
        if sn['AvailabilityZone'] == 'us-east-1a' or sn['AvailabilityZone'] == 'us-east-1b':
            subnets.append(sn['SubnetId'])

    load_balancer = create_load_balancer(elb_client, subnets, security_groups, target_groups)

    write_file_content(load_balancer['LoadBalancerDNS'])

    instances_ami = 'ami-08c40ec9ead489470'

    key_pair = create_key_pair(ec2_client, "key_pair")
    try:
        # cluster 1 instances
        create_instances(ec2_resource, instances_ami, "t2.large", "key_pair", "cluster1", subnets[0], 3, sg['GroupId'])
        create_instances(ec2_resource, instances_ami, "t2.large", "key_pair", "cluster1", subnets[1], 2, sg['GroupId'])

        # cluster 2 instances
        create_instances(ec2_resource, instances_ami, "m4.large", "key_pair", "cluster2", subnets[1], 2, sg['GroupId'])
        create_instances(ec2_resource, instances_ami, "m4.large", "key_pair", "cluster2", subnets[0], 2, sg['GroupId'])
        
        print("Instances created")
    except Exception as e:
        print(e)


    
    awake = False
    # for now number of instances are 1
    awake_instances = None
    # Wait for all instances to instanciate
    while awake is False:
        # Name filter used to prevent existing instances from interfering
        awake_instances = ec2_resource.instances.filter(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Name', 'Values': ['cluster1', 'cluster2']}
            ]
        )
        if len(list(awake_instances.all())) == 9:
            awake = True
        
        else:
            time.sleep(0.5)

    public_ips = [instance.public_ip_address for instance in awake_instances.all()]

    # List of commands to run on the instances
    commands = [
        'chmod 777 install.sh',
        "./install.sh",
        'sudo apt-get update -y',
        "echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections",
        'sudo apt-get install -y -q',
        'sudo apt-get install python3-pip -y',
        'sudo apt-get install nginx -y',
        'sudo apt-get install gunicorn3 -y',
        'sudo pip3 install flask',
        'sudo pip3 install ec2-metadata',
        'sudo mv nginxconfig /etc/nginx/sites-enabled',
        "sudo sed -i 's/# server_names_hash_bucket_size 64;/server_names_hash_bucket_size 128;/g' /etc/nginx/nginx.conf",
        'sudo service nginx restart',
        'sudo apt install screen -y',
        '/usr/bin/screen -dm gunicorn3 app:app'
    ]

    folder_path = os.path.abspath("flask_application")
    files = [
        os.path.join(folder_path, "app.py"),
        os.path.join(folder_path, "nginxconfig"),
        os.path.join(folder_path, "install.sh")
    ]

    time.sleep(60)

    deploy_threads = []
    for ip in public_ips:
        deploy_thread = Thread(target=start_deployment, args=(ip, files, commands, key_pair["KeyMaterial"]))
        deploy_thread.start()
        deploy_threads.append(deploy_thread)

    for deploy_thread in deploy_threads:
        deploy_thread.join()

    cluster1_instances = awake_instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['cluster1']}]
    )

    cluster2_instances = awake_instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['cluster2']}]
    )

    cluster1_targets_ids = []
    for ins in cluster1_instances.all():
        cluster1_targets_ids.append({'Id': ins.id})

    cluster2_targets_ids = []
    for ins in cluster2_instances.all():
        cluster2_targets_ids.append({'Id': ins.id})

    threads = [
        Thread(target=add_instance_to_target_group, args=[elb_client, target_groups[0], cluster1_targets_ids]),
        Thread(target=add_instance_to_target_group, args=[elb_client, target_groups[1], cluster2_targets_ids])
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Set up completed")

    load_balancer_dns = load_balancer["LoadBalancerDNS"]

    # sending requests to the endpoints.
    threads = [
        Thread(target=send_requests_thread1, args=[load_balancer_dns]),
        Thread(target=send_requests_thread2, args=[load_balancer_dns])
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Requests were sent")
    try:
        # Get all instances ids
        instances_ids = []
        for instance in ec2_resource.instances.filter(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Name', 'Values': ['cluster1', 'cluster2']}
            ]
        ):
            instances_ids.append(instance.id)
    
        getStatistics(session,instances_ids)

    except Exception as e:
        print(e)


    # Tear down
    print("Tearing down")
    delete_load_balancer(elb_client, load_balancer)

    remove_instance_from_target_group(elb_client, target_groups[0], cluster1_targets_ids)
    remove_instance_from_target_group(elb_client, target_groups[1], cluster1_targets_ids)

    for target_group in target_groups:
        delete_target_group(elb_client, target_group)

    terminate_instances(ec2_resource, cluster1_targets_ids)
    terminate_instances(ec2_resource, cluster2_targets_ids)

    ec2_client.delete_key_pair(KeyName="key_pair")

    delete_security_group(ec2_client, sg['GroupId'])

    print("Successfully deleted")
