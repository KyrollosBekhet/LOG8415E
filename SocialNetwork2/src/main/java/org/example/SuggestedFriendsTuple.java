package org.example;

import org.apache.hadoop.io.Writable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.Objects;

import static java.lang.Math.max;
import static java.lang.Math.min;

public class SuggestedFriendsTuple {

    private int id1;
    private int id2;

    public static SuggestedFriendsTuple createSuggestedFriend(String id1, String id2){
        SuggestedFriendsTuple s = new SuggestedFriendsTuple();
        s.id1 = min(Integer.parseInt(id1), Integer.parseInt(id2));
        s.id2 = max(Integer.parseInt(id1), Integer.parseInt(id2));
        return s;
    }

    public String toString(){
        return String.format("%d %d", id1, id2);
    }
    public String getId1(){
        return Integer.toString(id1);
    }

    public String getId2(){
        return Integer.toString(id2);
    }
}
