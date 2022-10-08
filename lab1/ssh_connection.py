from tokenize import String
import paramiko
from scp import SCPClient
import os


def start_deployement(ip, deployement_script, commands):
    """
    This function starts the deployement process for the instance with the provided ip address.
    The deployement script is runned on the instance. The provided deployement commands are also 
    runned on the instance before closing the connection.
    """
    connection = instance_connection(ip)
    transfer_file(connection, deployement_script)
    run_commands(connection, commands)
    connection.close()


def instance_connection(instance_ip):
    """
    This function initialize a connection with the ec2 instance.
    """
    ssh_username = "ubuntu"
    ssh_key_file = os.path.abspath("labsuser.pem")

    rsa_key = paramiko.RSAKey.from_private_key_file(ssh_key_file)

    ssh_connection = paramiko.SSHClient()
    ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connection.connect(hostname=instance_ip, username=ssh_username,
                           pkey=rsa_key, allow_agent=False, look_for_keys=False)

    return ssh_connection


def transfer_file(ssh_connection, file):
    """
    Initializes a SCP connection using a SSH connection and tranfert the file to the instance connected 
    to the session.
    """
    scp_connection = SCPClient(ssh_connection.get_transport())
    scp_connection.put(file, recursive=True, remote_path='/home/ubuntu')
    scp_connection.close()


def run_commands(ssh_connection, commands):
    """
    Executes a list of bash commands in the instance connected to the SSH session.
    """
    for command in commands:
        print("running command: {}".format(command))
        _, stdout, stderr = ssh_connection.exec_command(command)
        print(stdout.read())
        print(stderr.read())
