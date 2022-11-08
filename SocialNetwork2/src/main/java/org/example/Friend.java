package org.example;

import org.apache.hadoop.io.Writable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class Friend implements Writable {

    private int id;
    private long mutualFriends;

    public void incrementMutualFriends(long increment){
        mutualFriends += increment;
    }

    public long getMutualFriends(){
        return mutualFriends;
    }

    public String getId(){
        return Integer.toString(id);
    }

    Friend(String id, int mutualFriends){
        this.id = Integer.parseInt(id);
        this.mutualFriends = mutualFriends;
    }

    Friend(){}

    /**
     * @param dataOutput
     * @throws IOException
     */
    @Override
    public void write(DataOutput dataOutput) throws IOException {
        dataOutput.writeInt(id);
        dataOutput.writeLong(mutualFriends);
    }

    /**
     * @param dataInput
     * @throws IOException
     */
    @Override
    public void readFields(DataInput dataInput) throws IOException {
        id = dataInput.readInt();
        mutualFriends = dataInput.readLong();
    }

    public Friend copy(){
        return new Friend(Integer.toString(id), (int)mutualFriends);
    }
}
