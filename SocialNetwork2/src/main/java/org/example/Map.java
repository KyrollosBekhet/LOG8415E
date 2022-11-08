package org.example;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;

public class Map extends Mapper<LongWritable, Text, Text, IntWritable> {
    private static IntWritable one = new IntWritable(1);
    private static HashSet<String> alreadyFriends = new HashSet<>();

    public void map(LongWritable key, Text value,
                    Context output) throws IOException, InterruptedException {
        String user = "";
        String line = value.toString();
        try {
            String[] split = line.split("\t");
            user = split[0];
            String[] friends = split[1].split(",");
            for(int j = 0; j< friends.length; j++) {
                String currentFriend = friends[j];
                for (int i = j + 1; i < friends.length; i++) {
                    emit(output,SuggestedFriendsTuple.createSuggestedFriend(currentFriend, friends[i]));
                }
                addAlreadyFriend(SuggestedFriendsTuple.createSuggestedFriend(user, currentFriend).toString());
            }
        } catch (ArrayIndexOutOfBoundsException e) {
        }

    }

    public static void  addAlreadyFriend(String s){
            alreadyFriends.add(s);
    }

    public static boolean containsFriend(String s){
        return alreadyFriends.contains(s);
    }

    private void emit(Context output, SuggestedFriendsTuple s) throws IOException, InterruptedException {
            output.write(new Text(s.toString()), one);
    }
}
