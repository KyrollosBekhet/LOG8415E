from flask import Flask, jsonify
from ec2_metadata import ec2_metadata

app = Flask(__name__)

@app.route('/cluster1')
def hello_from_instance_cluster1():
    return jsonify('Hello from cluster 1 instance: {}'.format(ec2_metadata.instance_id))


@app.route('/cluster2')
def hello_from_instance_cluster2():
    return jsonify('Hello from cluster 2 instance: {}'.format(ec2_metadata.instance_id))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
