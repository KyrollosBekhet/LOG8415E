package org.example;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class FriendSuggestionTokenizer extends Mapper<LongWritable, Text, Text, Friend> {

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        //try{
            String[] split = line.split("\t");
            int count = Integer.parseInt(split[1]);
            String[] sugg = split[0].split(" ");
            Friend suggestion1 = new Friend(sugg[0], count);
            Friend suggestion2 = new Friend(sugg[1], count);
            context.write(new Text(sugg[0]), suggestion2);
            context.write(new Text(sugg[1]), suggestion1);
        //} catch(NullPointerException e){ System.out.println(e.getMessage());}

    }
}
