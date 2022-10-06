# Before executing these commands make sure to have all the needed files
# in your AWS instance
# First update the AMI
sudo apt-get update -y
# Make sure that python3 is iinstalled
sudo apt-get install python3 -y
# Install pip
sudo apt-get install python3-pip -y
# Install the nginx server
sudo apt-get install nginx -y
# Install the gunicorn (a package needed to deploy a fask server)
sudo apt-get install gunicorn3
# Install flask using pip
sudo pip3 install flask
# Install ec2-metadta (The python module used by the app to know the
# insatnce id)
sudo pip3 install ec2-metadata

# After adding the flaskapp file under /etc/nginx/sites-enabled inside
# the AWS instance execute this command
sudo service nginx restart # restarting nginx service to take in count
			   # the file that has been added to the
			   # directory /etc/nginx/sites-enabled

# Go inside the directory where your flask application is and execute
gunicorn3 app:app 
