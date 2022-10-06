import paramiko

# 172.31.89.53

ec2_instances = ['35.173.244.30']

ssh_username = "ubuntu"
ssh_key_file = "C:\\Users\\Philippe\\Documents\\POLYTECHNIQUE\\LOG8415\\LOG8415E\\lab1\\labsuser.pem"

commands = [
    "echo starting ...",
    "sudo apt-get update",
    "echo hi",
    "whoami",
    "hostname"
]

k = paramiko.RSAKey.from_private_key_file(ssh_key_file)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(hostname=ec2_instances[0], username=ssh_username, pkey=k, allow_agent=False, look_for_keys=False)

for command in commands:
    print("running command: {}".format(command))
    stdin , stdout, stderr = c.exec_command(command)
    print(stdout.read())
    print(stderr.read())

c.close()