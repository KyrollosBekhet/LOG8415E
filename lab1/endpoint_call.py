from importlib.resources import path
from threading import Thread
from itertools import cycle
import traceback
import requests
import time


def call_endpoint_http(load_balancer_dns, path):
    url = "http://{}/{}".format(load_balancer_dns, path)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    print(r.status_code)
    print(r.json())


def round_robin_call_endpoint_http(load_balancer_dns, turns):
    """
    This function dispatch HTTP endpoint call between the two clusters.
    """
    try:
        # Calling next on this object alternate between 0 and 1
        round_robin = cycle(range(2))
        paths = ["cluster1", "cluster2"]
        for _ in range(0, turns):
            call_endpoint_http(load_balancer_dns=load_balancer_dns, path=paths[next(round_robin)])
    except Exception as ex:
        print("Exception thrown thread {}.\n with stacktrace".format(str(Thread.name)))
        traceback.print_exc()
    finally:
        exit(None)


def send_requests_thread1(load_balancer_dns):
    """
     Sends 1000 requests divided equaly between the clusters.
     """
    round_robin_call_endpoint_http(load_balancer_dns, 500)


def send_requests_thread2(load_balancer_dns):
    """
    Sends an equal amount of HTTP requests to both clusters.
    Starts by sending 500 requests. 
    Then waits 60 seconds and sends 1000 more requests.
    """
    round_robin_call_endpoint_http(load_balancer_dns, 500)
    time.sleep(60)
    round_robin_call_endpoint_http(load_balancer_dns, 1000)


if __name__ == "__main__":
    threads = []
    for i in range(0, 1000):
        threads.append(Thread(target=call_endpoint_http, args=("lb-619373195.us-east-1.elb.amazonaws.com", "cluster1")))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
