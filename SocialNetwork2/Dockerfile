from ubuntu:latest
SHELL ["/bin/bash", "-c"] 
RUN apt-get update
RUN apt-get install default-jdk -y
RUN apt-get install default-jre -y
RUN apt-get install wget -y
RUN wget https://dlcdn.apache.org/hadoop/common/stable/hadoop-3.3.4.tar.gz
RUN tar -xf hadoop-3.3.4.tar.gz -C /usr/local/
RUN echo 'export HADOOP_HOME="/usr/local/hadoop-3.3.4"' >> ~/.profile
RUN echo 'export PATH="$HADOOP_HOME/bin":$PATH' >> ~/.profile
RUN echo 'export JAVA_HOME="$(readlink -f /usr/bin/java| sed "s:bin/java::")"' >> ~/.profile
RUN echo 'export PATH="$JAVA_HOME/bin":$PATH' >> ~/.profile
RUN source ~/.profile
COPY soc-LiveJournal1Adj.txt .
RUN hdfs dfs -mkdir input_social_networking;
RUN hdfs dfs -copyFromLocal soc-LiveJournal1Adj.txt input_social_networking;
COPY src/main/java/org/example/*.java code/.
RUN export CLASSPATH=`hadoop classpath`:.:
RUN javac -d social_network_classes code/*.java
RUN jar -cvf SocialNetwork.jar -C social_network_classes/ .
