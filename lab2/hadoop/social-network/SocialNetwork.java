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
	    //System.out.println(line);
	    try {
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
	    } catch(ArrayIndexOutOfBoundsException e){  }
	    //catch(IOException e){System.out.println("IO error"); throw new IOException(e.toString());}

         }
    }

    public static class Combine extends MapReduceBase implements Reducer<Text, Friend, Text, Friend>{
        public void reduce(Text key, Iterator<Friend> values,
                           OutputCollector<Text, Friend> output, Reporter reporter) throws IOException{
            Set<String> alreadyFriends = new HashSet<String>();
            Set<String> notFriends = new HashSet<String>();
            while(values.hasNext()) {
                Friend user = values.next();
                if (user.isAlreadyFriend()) {
                    alreadyFriends.add(user.getId());
                } else {
                    notFriends.add(user.getId());
                }
            }

            notFriends.removeAll(alreadyFriends);
            for(String sugg: notFriends){
                output.collect(key, new Friend(sugg, false));
            }
        }
    }

    public static class Reduce extends MapReduceBase implements Reducer<Text, Friend, Text, Text>{
        public void reduce(Text key, Iterator<Friend> values,
                           OutputCollector<Text, Text> output, Reporter reporter) throws IOException{
            //Set<String> alreadyFriends = new HashSet<String>();
            //Set<String> notFriends = new HashSet<String>();
            String textString = "    ";
	        while(values.hasNext()) {
                Friend user = values.next();
		        textString += user.getId()+" ,";
   
            }
            Text outputText = new Text(textString);
            output.collect(key, outputText);
        }
    }

    public static void main(String[] args) throws Exception {
        JobConf conf = new JobConf(SocialNetwork.class);
        conf.setJobName("socialnetwork");
	    conf.setMapOutputKeyClass(Text.class);
        conf.setMapOutputValueClass(Friend.class);
        
	    conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(Text.class);
	
        conf.setMapperClass(Map.class);
        conf.setCombinerClass(Combine.class);
        conf.setReducerClass(Reduce.class);

        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);

        FileInputFormat.setInputPaths(conf, new Path(args[0]));
        FileOutputFormat.setOutputPath(conf, new Path(args[1]));

        JobClient.runJob(conf);
      }
}

