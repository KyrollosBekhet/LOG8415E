package org.example;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Iterator;

public class GetSuggestions extends Reducer<Text, Friend, Text, Text> {

    public void reduce(Text key, Iterable<Friend> iterable, Context context) throws IOException, InterruptedException {

        ArrayList<Friend> suggestions = new ArrayList<>();
        Iterator<Friend> i = iterable.iterator();
        while(i.hasNext()){
            Friend sugg = i.next().copy();
            if(!suggestions.contains(sugg))
                suggestions.add(sugg);
        }

        suggestions.sort(Comparator.comparing(Friend::getMutualFriends).reversed());

        String result = "";
        for(int j = 0; j< 10 && j< suggestions.size(); j++){
            if(j !=0) result += ",";
            result += suggestions.get(j).getId();
        }

        context.write(key, new Text(result));
    }
}
