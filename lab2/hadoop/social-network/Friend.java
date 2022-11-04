package socialnetwork;
import org.apache.hadoop.io.*;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class Friend implements Writable{
    private int id;
    private boolean alreadyFriend;

    Friend(){}
    Friend(String id, boolean alreadyFriiend){
        this.id = Integer.parseInt(id);
        this.alreadyFriend = alreadyFriiend;
    }

    public void readFields(DataInput in) throws IOException {
        id = in.readInt();
        alreadyFriend = in.readBoolean();
    }

    public void write(DataOutput out) throws IOException{
        out.writeInt(id);
        out.writeBoolean(alreadyFriend);
    }

    public static Friend read(DataInput in) throws IOException{
        Friend f = new Friend();
        f.readFields(in);
        return f;
    }
    public String getId() {
        return String.format("%d",id);
    }

    public boolean isAlreadyFriend() {
        return alreadyFriend;
    }
}
