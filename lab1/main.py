from ipaddress import ip_address
import time

from ELB_setup import *
import boto3
from ELB_teardown import *
from security_group import *
from instances import *
from ssh_connection import *
from threading import Thread
from endpoint_call import *

from nginx_file_writter import *

""" 
TODO: Remove the main function the goal of this method is to test the creation of the load balancer
 and target groups. Also to identify what is needed to create the load balancer
"""


def main():
    # Creating session using default credentials and configuration.
    session = boto3.Session(profile_name='default')

    elb_client = session.client('elbv2')
    ec2_client = session.client('ec2')
    ec2_resource = session.resource('ec2')

    #default_security_group = ec2_client.describe_security_groups(
     #  GroupNames=['default'])['SecurityGroups'][0]

    vpcs = ec2_client.describe_vpcs()
    vpc_id = vpcs.get('Vpcs', [{}])[0].get('VpcId', '')
    sg = create_security_group(ec2_client, vpc_id)
    cluster1 = create_target_groups(elb_client, "cluster1", vpc_id)[
        "TargetGroups"][0]
    cluster2 = create_target_groups(elb_client, "cluster2", vpc_id)[
        "TargetGroups"][0]
    target_groups = [cluster1['TargetGroupArn'], cluster2['TargetGroupArn']]

    security_groups = [sg['GroupId']]

    sn_all = ec2_client.describe_subnets()
    subnets = []
    for sn in sn_all['Subnets']:
        if sn['AvailabilityZone'] == 'us-east-1a' or \
                sn['AvailabilityZone'] == 'us-east-1b':
            subnets.append(sn['SubnetId'])

    load_balancer = create_load_balancer(elb_client, subnets,
                                         security_groups, target_groups)

    write_file_content(load_balancer['LoadBalancerDNS'])

    instances_ami = 'ami-08c40ec9ead489470'

    private_key = ec2_client.describe_key_pairs()['KeyPairs'][0]
    try:
        create_instances(ec2_resource, instances_ami, "t2.micro",
                         private_key["KeyName"], "cluster1", subnets[0], 1, sg['GroupId'])
        create_instances(ec2_resource, instances_ami, "t2.micro",
                         private_key["KeyName"], "cluster2", subnets[1], 1, sg['GroupId'])
        print("Instances created")
    except Exception as e:
        print(e)

    awake = False
    # for now number of instances are 1
    awake_instances = None
    while awake is False:
        # Name filter used to prevent existing instances from interfering
        awake_instances = ec2_resource.instances.filter(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Name', 'Values': ['cluster1', 'cluster2']}
            ]
        )
        if len(list(awake_instances.all())) == 2:
            awake = True

    public_ips = [instance.public_ip_address for instance in awake_instances.all()]

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
        "sudo sed -i 's/#server_names_hash_bucket_size 64;/server_names_hash_bucket_size 128;/g' /etc/nginx/nginx.conf",
        'sudo service nginx restart',
        'sudo apt install screen -y',
        '/usr/bin/screen -d -m -S gunicorn3 app:app 2> /dev/null &']
    folder_path = os.path.abspath("flask_application")
    files = [os.path.join(folder_path, "app.py"), os.path.join(folder_path, "nginxconfig"),
             os.path.join(folder_path, "install.sh")]

    time.sleep(30)
    threads=[]
    for ip in public_ips:
        #thread = Thread(target=start_deployement, args=((ip, files, commands)))
        #thread.start()
        #threads.append(thread)
        start_deployement(ip, files, commands)
    

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

    add_instance_to_target_group(
        elb_client, target_groups[0], cluster1_targets_ids)

    add_instance_to_target_group(
        elb_client, target_groups[1], cluster2_targets_ids
    )

    print("Set up completed")
    # wait 30 seconds to simulate an interruption

    time.sleep(5)
    load_balancer_dns = load_balancer["LoadBalancerDNS"]
    # calling endpoints. TODO: Modify this code if needed
    threads = [Thread(target=call_endpoint_http_thread1, args=(load_balancer_dns)),
               Thread(target=call_endpoint_http_thread2, args=(load_balancer_dns))]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Tear down
    delete_load_balancer(elb_client, load_balancer)

    remove_instance_from_target_group(elb_client, target_groups[0],
                                      cluster1_targets_ids)

    remove_instance_from_target_group(elb_client, target_groups[1],
                                      cluster1_targets_ids)
    for target_group in target_groups:
        delete_target_group(elb_client, target_group)

    terminate_instances(ec2_resource, cluster1_targets_ids)
    terminate_instances(ec2_resource, cluster2_targets_ids)
    # time.sleep(5)

    delete_security_group(ec2_client, sg['GroupId'])
    print("Successfully deleted")


main()
