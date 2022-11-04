sudo sed -i 's/#$nrconf{restart} = '"'"'i'"'"';/$nrconf{restart} = '"'"'a'"'"';/g' /etc/needrestart/needrestart.conf;
sudo apt-get install default-jdk -y;
sudo apt-get install default-jre -y;
sudo apt-get install python3-pip -y;
sudo apt-get install python3-venv -y;
wget https://dlcdn.apache.org/hadoop/common/stable/hadoop-3.3.4.tar.gz;
sudo tar -xf hadoop-3.3.4.tar.gz -C /usr/local/;
echo 'export HADOOP_HOME="/usr/local/hadoop-3.3.4"' >> ~/.profile;
echo 'export PATH="$HADOOP_HOME/bin":$PATH' >> ~/.profile;
echo 'export JAVA_HOME="$(readlink -f /usr/bin/java| sed "s:bin/java::")"' >> ~/.profile;
echo 'export PATH="$JAVA_HOME/bin":$PATH' >> ~/.profile;
source ~/.profile;
sudo python3 -m venv venv;
source venv/bin/activate;
pip install pyspark;
hdfs dfs -mkdir input;
hdfs dfs -copyFromLocal 4300.txt input
hadoop jar /usr/local/hadoop-3.3.4/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.4.jar wordcount input output
echo "execute ls"
ls;



