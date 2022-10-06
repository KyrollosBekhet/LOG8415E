from flask import Flask
from ec2_metadata import ec2_metadata

app = Flask(__name__)

@app.route('/cluster1')
def hello_from_instance():
    return 'Hello from instance: {}'.format(ec2_metadata.instance_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
