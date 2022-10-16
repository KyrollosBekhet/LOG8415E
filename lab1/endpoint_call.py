import traceback
import requests
from threading import Thread
import time


def call_endpoint_http(load_balancer_dns, path):
    url = "http://{}/{}".format(load_balancer_dns, path)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    print(r.status_code)
    print(r.json())


def call_endpoint_http_thread1(load_balancer_dns):
    try:
        paths = ["cluster1", "cluster2"]
        for i in range(0, 1000):
            if i % 2 == 0:
                call_endpoint_http(load_balancer_dns=load_balancer_dns, path=paths[0])
            else:
                call_endpoint_http(load_balancer_dns=load_balancer_dns, path=paths[1])

    except Exception as ex:
        print("Exception thrown thread {}.\n with stacktrace"
              .format(str(Thread.name)))
        traceback.print_exc()
    finally:
        exit(None)


def call_endpoint_http_thread2(load_balancer_dns):
    try:
        paths = ["cluster1", "cluster2"]
        for i in range(0, 500):
            if i % 2 == 0:
                call_endpoint_http(load_balancer_dns=load_balancer_dns, path=paths[1])

            else:
                call_endpoint_http(load_balancer_dns=load_balancer_dns, path=paths[0])

        time.sleep(1)

        for i in range(0, 1000):
            if i % 2 == 0:
                call_endpoint_http(load_balancer_dns=load_balancer_dns, path=paths[1])
            else:
                call_endpoint_http(load_balancer_dns=load_balancer_dns, path=paths[0])

    except Exception as ex:
        print("Exception thrown thread {}.\n with stacktrace"
              .format(str(Thread.name)))
        traceback.print_exc()
    finally:
        exit(None)

if __name__ == "__main__":
    threads = []
    for i in range(0, 1000):
        threads.append(Thread(target=call_endpoint_http, args=("lb-619373195.us-east-1.elb.amazonaws.com", "cluster1")))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
