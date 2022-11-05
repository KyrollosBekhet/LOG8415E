#sudo sed -i 's/#$nrconf{restart} = '"'"'i'"'"';/$nrconf{restart} = '"'"'a'"'"';/g' /etc/needrestart/needrestart.conf;
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
pip3 install pyspark --user;
pip3 install pandas --user;
hdfs dfs -mkdir input_social_networking;
hdfs dfs -mkdir input_text_page;
hdfs dfs -copyFromLocal LOG8415E/lab2/hadoop/social-network/soc-LiveJournal1Adj.txt input_social_networking;
hdfs dfs -copyFromLocal 4300.txt input_text_page;
cd LOG8415E && git checkout automate_deployment && cd ..
echo "# output hadoop time for 4300.txt" >> time_results.txt
export CLASSPATH=`hadoop classpath`:.:
javac -d word_count_classes LOG8415E/lab2/hadoop/wordcount/WordCount.java
jar -cvf wordCount.jar -C word_count_classes/ .
{ time hadoop jar wordCount.jar org.myorg.WordCount input_text_page output_text_page 2>1; } 2>> time_results.txt

echo "# output linux time for 4300.txt" >>time_results.txt
{ time cat 4300.txt | tr ' ' '\n' | sort | uniq -c 2>1; } 2>> time_results.txt

export CLASSPATH=`hadoop classpath`:.:
javac -d socialnetwork_classes LOG8415E/lab2/hadoop/social-network/Friend.java LOG8415E/lab2/hadoop/social-network/SocialNetwork.java
jar -cvf socialnetwork.jar -C socialnetwork_classes/ .
hadoop jar socialnetwork.jar socialnetwork.SocialNetwork input_social_networking output_social_networking_results
mv output_social_networking_results/part-00000 ./friends_suggestion_solution.txt
#python3 LOG8415E/lab2/spark/word_count.py
#time hadoop jar /usr/local/hadoop-3.3.4/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.4.jar wordcount input/4300.txt output;




