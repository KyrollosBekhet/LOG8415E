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
import os


def write_file_content(dns):
    ret = "server " + "{\n" + "\t listen 80;\n" +\
          "\t server_name {};\n".format(dns) + "\n" +\
          "\t location" + "/ {\n" +\
          "\t \t proxy_pass http://127.0.0.1:8000;\n"\
          + "\t }\n" \
          + "\t".join("}")
    print(ret)
    path_folder = os.path.abspath('flask_application')
    path_file = os.path.join(path_folder, 'nginxconfig')
    f = open(path_file, "w")
    f.write(ret)
    f.close()


if __name__ == "__main__":
    write_file_content("lb-619373195.us-east-1.elb.amazonaws.com")
