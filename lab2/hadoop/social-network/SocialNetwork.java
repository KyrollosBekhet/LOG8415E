package socialnetwork;

import java.io.IOException;
import java.util.*;

import javax.xml.soap.Text;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;

public class SocialNetwork {

    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, Friend> {

        private Text user;

        /**
         * Each mapper will read a line which is the value. This value presents a
         * <User><TAB><Friends>.
         * Each user will suggest all his friends to a friend while saying to that
         * friend that he
         * is his friend via the boolean attribute isAlreadyFriends
         * 
         * @param key      The key allocated to a mapper instance.
         * @param value    A line from the dataset containing a user and its friends.
         * @param output   A <Text, Friend> key-value pair representing a friend for the
         *                 User
         * @param reporter Reports progress and status information while also providing
         *                 applications
         *                 a way to update Counters.
         * @throws IOException
         * 
         */
        public void map(LongWritable key, Text value,
                OutputCollector<Text, Friend> output, Reporter reporter) throws IOException {
            String line = value.toString();
                
            try {
                String[] userFriends = line.split("\t"); // Separate <User> and <Friends> using <TAB>
                user = new Text(userFriends[0]);
                String[] friends = userFriends[1].split(",");

                StringTokenizer tokenizer = new StringTokenizer(userFriends[1], ",");
                Text currentFriend = new Text();

                while (tokenizer.hasMoreTokens()) {
                    currentFriend.set(tokenizer.nextToken());
                    // Create relations between current friend and the other friends.
                    for (int i = 0; i < friends.length; i++) {
                        // Cannot be friend with itself
                        if (!friends[i].equals(currentFriend.toString())) {
                            output.collect(currentFriend, new Friend(friends[i], false, 1));
                        }
                    }
                    output.collect(currentFriend, new Friend(user.toString(), true, 1));
                }
            } catch(IndexOutOfBoundsException ex) {
                System.out.println("user doesn't have a friend");
            }
        }
    }

    public static class Reduce extends MapReduceBase implements Reducer<Text, Friend, Text, Text> {
        /***
         * The reducer will separate the friends from the suggested friends. It will
         * sort based on the count of mutual friends and return the 10 most suggested
         * friends for each user
         * 
         * @param key      The user handled by the reducer
         * @param values   A collection of Friend object containing both friends and
         *                 suggested friends
         * @param output   A <User><TAB><Recommendation> containing the user and at most
         *                 10 friends
         *                 recommendations based on the count of mutual friends.
         * @param reporter Reports progress and status information while also providing
         *                 applications
         *                 a way to update Counters.
         * @throws IOException
         */
        public void reduce(Text key, Iterator<Friend> values,
                OutputCollector<Text, Text> output, Reporter reporter) throws IOException {

            HashMap<String, Friend> alreadyFriends = new HashMap<>();
            HashMap<String, Friend> notFriends = new HashMap<>();
            String recommendations = "\t";

            while (values.hasNext()) {
                Friend user = values.next();

                if (user.isAlreadyFriend()) {
                    if (alreadyFriends.containsKey(user.getId())) {
                        Friend existingSugg = alreadyFriends.get(user.getId());
                        existingSugg.incrementMutualFriends(user.getMutualFriends());
                        alreadyFriends.replace(user.getId(), existingSugg);
                    } else {
                        alreadyFriends.put(user.getId(), user.copy());
                    }
                } else if (notFriends.containsKey(user.getId())) {
                    Friend existingSugg = notFriends.get(user.getId());
                    existingSugg.incrementMutualFriends(user.getMutualFriends());
                    notFriends.replace(user.getId(), existingSugg);
                } else {
                    notFriends.put(user.getId(), user.copy());
                }
            }

            ArrayList<Friend> notFriendsSet = new ArrayList<>();

            for (Map.Entry<String, Friend> entry : notFriends.entrySet()) {
                if (!alreadyFriends.containsKey(entry.getKey())) {
                    notFriendsSet.add(entry.getValue().copy());
                }
            }

            // Sorting in reverse of mutual friends to get recommendations with the most
            // friends in common first.
            notFriendsSet.sort(Comparator.comparing(Friend::getMutualFriends).reversed());

            // Appending the 10 recommendations with the most friends in common.
            for (int i = 0; i < 10 && i < notFriendsSet.size(); i++) {
                if (i != 0) {
                    recommendations += ",";
                }
                recommendations += notFriendsSet.get(i).getId();
            }

            Text outputText = new Text(recommendations);
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
        conf.setReducerClass(Reduce.class);

        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);

        FileInputFormat.setInputPaths(conf, new Path(args[0]));
        FileOutputFormat.setOutputPath(conf, new Path(args[1]));

        JobClient.runJob(conf);
    }
}