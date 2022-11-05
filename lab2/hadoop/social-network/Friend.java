package socialnetwork;
import org.apache.hadoop.io.*;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class Friend implements Writable{
    private int id;
    private boolean alreadyFriend;
    private long mutualFriends;
    Friend(){}
    Friend(String id, boolean alreadyFriend, long mutualFriends){
        this.id = Integer.parseInt(id);
        this.alreadyFriend = alreadyFriend;
        this.mutualFriends = mutualFriends;
    }

    public void readFields(DataInput in) throws IOException {
        id = in.readInt();
        alreadyFriend = in.readBoolean();
        mutualFriends = in.readLong();
    }

    public void write(DataOutput out) throws IOException{
        out.writeInt(id);
        out.writeBoolean(alreadyFriend);
        out.writeLong(mutualFriends);
    }

    public static Friend read(DataInput in) throws IOException{
        Friend f = new Friend();
        f.readFields(in);
        return f;
    }
    public String getId() {
        return String.format("%d",id);
    }

    public long getMutualFriends() {
        return mutualFriends;
    }

    public void incrementMutualFriends(long incrementFactor){
        mutualFriends += incrementFactor;
    }

    public boolean isAlreadyFriend() {
        return alreadyFriend;
    }

    public Friend copy(){
    	return new Friend(Integer.toString(id), alreadyFriend, mutualFriends);
    }
}
