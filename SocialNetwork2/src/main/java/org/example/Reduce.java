package org.example;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.Iterator;

public class Reduce extends Reducer<Text, IntWritable, Text, IntWritable> {
    /**
     * @param suggestedFriendsTuple
     * @param iterator
     * @param outputCollector
     * @throws IOException
     */
    @Override
    public void reduce(Text suggestedFriendsTuple, Iterable<IntWritable> iterator,
                       Context outputCollector) throws IOException, InterruptedException {

        if(!Map.containsFriend(suggestedFriendsTuple.toString())){
            int sum = 0;
            for (IntWritable intWritable : iterator) {
                sum += intWritable.get();
            }
            outputCollector.write(suggestedFriendsTuple,
                    new IntWritable(sum));
        }

    }
}
