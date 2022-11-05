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

        /**
         *
         * @param key
         * @param value
         * @param output
         * @param reporter
         * @throws IOException
         * Each mapper will read a line which is the value. This value presents a user<TAB>friends
         * Each user will suggest all his friends to a friend while saying to that friend that he
         * is his friend via the boolean attribute isAlreadyFriends
         */
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
                        output.collect(currentFriend, new Friend(friends[i], false, 1));
                    }
                }
                output.collect(currentFriend, new Friend(user.toString(), true, 1));
            }
	    } catch(ArrayIndexOutOfBoundsException e){  }
	    //catch(IOException e){System.out.println("IO error"); throw new IOException(e.toString());}

         }
    }

    public static class Combine extends MapReduceBase implements Reducer<Text, Friend, Text, Friend>{
        /***
         *
         * @param key A user
         * @param values The list of suggested friends can be a current friend or not.
         * @param output
         * @param reporter
         * @throws IOException
         * This function counts the number of an iteration of a suggestion whether he/she is a friend or not
         */
        public void reduce(Text key, Iterator<Friend> values,
                           OutputCollector<Text, Friend> output, Reporter reporter) throws IOException{
            HashMap<String, Friend> notFriends = new HashMap<>();
            HashMap<String, Friend> friends = new HashMap<>();
            while(values.hasNext()) {
                Friend user = values.next();
                if(!user.isAlreadyFriend()){
                    if(notFriends.containsKey(user.getId())){
                        Friend existingUser = notFriends.get(user.getId());
                        existingUser.incrementMutualFriends(user.getMutualFriends());
                        notFriends.replace(user.getId(), existingUser);
                    }
                    else{
                        notFriends.put(user.getId(), user.copy());
                    }
                }
                else{
                    if(friends.containsKey(user.getId())){
                        Friend existingUser = friends.get(user.getId());
                        existingUser.incrementMutualFriends(user.getMutualFriends());
                        friends.replace(user.getId(), existingUser);
                    }
                    else{
                        friends.put(user.getId(), user.copy());
                    }
                }

            }

            for(java.util.Map.Entry<String,Friend> sugg: notFriends.entrySet()){
                Friend value = sugg.getValue();
                output.collect(key, value.copy());
            }
            for(java.util.Map.Entry<String,Friend> sugg: friends.entrySet()){
                Friend value = sugg.getValue();
                output.collect(key, value.copy());
            }
        }
    }

    public static class Reduce extends MapReduceBase implements Reducer<Text, Friend, Text, Text>{
        /***
         *
         * @param key
         * @param values
         * @param output
         * @param reporter
         * @throws IOException
         * The reducer will separate the friends from the suggested friends.
         * It will sort based on the count of mutual friends and return the 10 most suggested friends
         * for each user
         */
        public void reduce(Text key, Iterator<Friend> values,
                           OutputCollector<Text, Text> output, Reporter reporter) throws IOException{
            HashMap<String,Friend> alreadyFriends = new HashMap<>();
            HashMap<String, Friend> notFriends = new HashMap<>();
            String textString = "    ";
	        while(values.hasNext()) {
                Friend user = values.next();
		        if(user.isAlreadyFriend()){
                    if(alreadyFriends.containsKey(user.getId())){
                            Friend existingSugg = alreadyFriends.get(user.getId());
                            existingSugg.incrementMutualFriends(user.getMutualFriends());
                            alreadyFriends.replace(user.getId(), existingSugg);
                    }
                    else{
                        alreadyFriends.put(user.getId(), user.copy());
                    }

                }
                else{
                    if(notFriends.containsKey(user.getId())){
                        Friend existingSugg = notFriends.get(user.getId());
                        existingSugg.incrementMutualFriends(user.getMutualFriends());
                        notFriends.replace(user.getId(), existingSugg);
                    }
                    else {
                        notFriends.put(user.getId(), user.copy());
                    }
                }
   
            }

            ArrayList<Friend> notFriendsSet = new ArrayList<>();
            for(java.util.Map.Entry<String, Friend> entry: notFriends.entrySet()){
                if(!alreadyFriends.containsKey(entry.getKey())){
                    notFriendsSet.add(entry.getValue().copy());
                }
            }

            notFriendsSet.sort(Comparator.comparing(Friend::getMutualFriends).reversed());
            for(int i = 0; i< 10 && i < notFriendsSet.size();i++){
                textString += notFriendsSet.get(i).getId()  + " suggested by " +
                        notFriendsSet.get(i).getMutualFriends()+ ",";
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

