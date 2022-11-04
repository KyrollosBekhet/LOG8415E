package socialnetwork;
import java.io.IOException;
import java.util.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;


public class SocialNetwork {
    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, Friend>{
        private Text user;

        public void map(LongWritable key, Text value,
         OutputCollector<Text,Friend> output, Reporter reporter ) throws IOException{
            String line = value.toString();
            String[] split = line.split("\t");
            user = new Text(split[0]);
            StringTokenizer tokenizer = new StringTokenizer(split[1],",");
            String[] friends = split[1].split(",");
            Text currentFriend = new Text();
            while(tokenizer.hasMoreTokens()){
                currentFriend.set(tokenizer.nextToken());
                for(int i = 0; i< friends.length; i++){
                    if(!friends[i].equals(currentFriend.toString())){
                        output.collect(currentFriend, new Friend(friends[i], false));
                    }
                }
                output.collect(currentFriend, new Friend(user.toString(), true));
            }

         }
    }

    public static class Reduce extends MapReduceBase implements Reducer<Text, Friend, Text, List<Text>>{
        public void reduce(Text key, Iterator<Friend> values,
                           OutputCollector<Text, Text> output, Reporter reporter) throws IOException{
            ArrayList<String> alreadyFriends = new ArrayList<String>();
            ArrayList<String> notFriends = new ArrayList<String>();
            while(values.hasNext()) {
                Friend user = values.next();
                if (user.isAlreadyFriend()) {
                    alreadyFriends.add(user.getId());
                } else {
                    notFriends.add(user.getId());
                }
            }

            notFriends.removeAll(alreadyFriends);
            Text outputText = new Text("    ");
            for(String sugg: notFriends){
                outputText.add(sugg.toString() + " ,");
            }
            output.collect(key, outputText);
        }
    }

    public static void main(String[] args) throws Exception {
        JobConf conf = new JobConf(SocialNetwork.class);
        conf.setJobName("socialnetwork");

        conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(Friend.class);

        conf.setMapperClass(Map.class);
        conf.setCombinerClass(Reduce.class);
        conf.setReducerClass(Reduce.class);

        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);

        FileInputFormat.setInputPaths(conf, new Path(args[0]));
        FileOutputFormat.setOutputPath(conf, new Path(args[1]));

        JobClient.runJob(conf);
      }
}

