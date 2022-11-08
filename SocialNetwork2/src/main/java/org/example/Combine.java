package org.example;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.Iterator;

public class Combine extends Reducer<Text, IntWritable, Text, IntWritable> {
    /**
     * @param suggestedFriendsTuple
     * @param iterator
     * @param outputCollector
     * @throws IOException
     */
    @Override
    public void reduce(Text suggestedFriendsTuple,
                       Iterable<IntWritable> iterator,
                       Context outputCollector) throws IOException, InterruptedException {
        int sum = 0;
        Iterator<IntWritable> i = iterator.iterator();

        while(i.hasNext()){
            sum += i.next().get();
        }

        if(sum % 2 != 0){
            outputCollector.write(suggestedFriendsTuple, new IntWritable(sum));
        }
        else{
            Map.addAlreadyFriend(suggestedFriendsTuple.toString());
        }
    }
}
