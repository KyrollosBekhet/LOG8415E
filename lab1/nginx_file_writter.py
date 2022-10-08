"""
file content:
server {
    listen 80;
    server_name lb-619373195.us-east-1.elb.amazonaws.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
  }
"""


def get_file_content(dns):
    ret = "server " + "{\n" + "\t listen 80;\n" +\
          "\t server_name {};\n".format(dns) + "\n" +\
          "\t location" + "/ {\n" +\
          "\t \t proxy_pass http://127.0.0.1:8000;\n"\
          + "\t }\n" \
          + "\t".join("}")
    print(ret)
    f = open("./flask_application/nginxconfig","w")
    f.write(ret)
    f.close()


if __name__ == "__main__":
    get_file_content("lb-619373195.us-east-1.elb.amazonaws.com")
