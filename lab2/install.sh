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
pip3 install pyspark --user;
pip3 install pandas --user;
pip3 install matplotlib --user;

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

#acquire dataSet
wget https://tinyurl.com/4vxdw3pa
wget https://tinyurl.com/kh9excea
wget https://tinyurl.com/dybs9bnk
wget https://tinyurl.com/datumz6m
wget https://tinyurl.com/j4j4xdw6
wget https://tinyurl.com/ym8s5fm4
wget https://tinyurl.com/2h6a75nk
wget https://tinyurl.com/vwvram8
wget https://tinyurl.com/weh83uyn

hdfs dfs -mkdir dataset
hdfs dfs -copyFromLocal 4vxdw3pa dataset
hdfs dfs -copyFromLocal kh9excea dataset
hdfs dfs -copyFromLocal dybs9bnk dataset
hdfs dfs -copyFromLocal datumz6m dataset
hdfs dfs -copyFromLocal j4j4xdw6 dataset
hdfs dfs -copyFromLocal ym8s5fm4 dataset
hdfs dfs -copyFromLocal 2h6a75nk dataset
hdfs dfs -copyFromLocal vwvram8 dataset
hdfs dfs -copyFromLocal weh83uyn dataset


# benchmarking hadoop
echo "#benchmarking hadoop results first run" >> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/4vxdw3pa output_benchamrking_hadoop_1_0 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/kh9excea output_benchamrking_hadoop_1_1 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/dybs9bnk output_benchamrking_hadoop_1_2 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/datumz6m output_benchamrking_hadoop_1_3 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/j4j4xdw6 output_benchamrking_hadoop_1_4 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/ym8s5fm4 output_benchamrking_hadoop_1_5 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/2h6a75nk output_benchamrking_hadoop_1_6 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/vwvram8 output_benchamrking_hadoop_1_7 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/weh83uyn output_benchamrking_hadoop_1_8 2>1; } 2>> benchmarking_time_results.txt

echo "benchmarking hadoop second run" >> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/4vxdw3pa output_benchamrking_hadoop_2_0 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/kh9excea output_benchamrking_hadoop_2_1 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/dybs9bnk output_benchamrking_hadoop_2_2 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/datumz6m output_benchamrking_hadoop_2_3 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/j4j4xdw6 output_benchamrking_hadoop_2_4 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/ym8s5fm4 output_benchamrking_hadoop_2_5 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/2h6a75nk output_benchamrking_hadoop_2_6 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/vwvram8 output_benchamrking_hadoop_2_7 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/weh83uyn output_benchamrking_hadoop_2_8 2>1; } 2>> benchmarking_time_results.txt

echo "benchmarking hadoop third run" >> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/4vxdw3pa output_benchamrking_hadoop_3_0 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/kh9excea output_benchamrking_hadoop_3_1 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/dybs9bnk output_benchamrking_hadoop_3_2 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/datumz6m output_benchamrking_hadoop_3_3 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/j4j4xdw6 output_benchamrking_hadoop_3_4 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/ym8s5fm4 output_benchamrking_hadoop_3_5 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/2h6a75nk output_benchamrking_hadoop_3_6 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/vwvram8 output_benchamrking_hadoop_3_7 2>1; } 2>> benchmarking_time_results.txt
{ time hadoop jar wordCount.jar org.myorg.WordCount dataset/weh83uyn output_benchamrking_hadoop_3_8 2>1; } 2>> benchmarking_time_results.txt

#spark benchmarking

echo "benchmarking spark first run" >> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/4vxdw3pa 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/kh9excea 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/dybs9bnk 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/datumz6m 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/j4j4xdw6 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/ym8s5fm4 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/2h6a75nk 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/vwvram8 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/weh83uyn 2>1; } 2>> benchmarking_time_results.txt

echo "benchmarking spark second run" >> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/4vxdw3pa 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/kh9excea 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/dybs9bnk 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/datumz6m 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/j4j4xdw6 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/ym8s5fm4 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/2h6a75nk 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/vwvram8 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/weh83uyn 2>1; } 2>> benchmarking_time_results.txt

echo "benchmarking spark third run" >> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/4vxdw3pa 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/kh9excea 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/dybs9bnk 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/datumz6m 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/j4j4xdw6 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/ym8s5fm4 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/2h6a75nk 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/vwvram8 2>1; } 2>> benchmarking_time_results.txt
{ time python3 LOG8415E/lab2/spark/word_count.py dataset/weh83uyn 2>1; } 2>> benchmarking_time_results.txt

python3 LOG8415E/lab2/plot.py





