import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum
import os
import time

def generate_word_count(path, name, result_dir="results"):
    spark = SparkSession.builder.getOrCreate()

    # Create a DataFrame from the text file
    text_file = spark.sparkContext.textFile(path)
    
    start = time.time()

    # Run WordCount pipeline from https://spark.apache.org/examples.html
    counts = text_file.flatMap(lambda line: line.split(" ")) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)

    end = time.time()

    # Convert pipeline back to DataFrame
    df_result = counts.toDF(["word", "count"])

    word_count = df_result.select(_sum('count')).alias('word_count').collect()[0][0]

    print("MapReduce spent {} second(s) on file {} with {} words".format(end - start, name, word_count))

    # Create results destination directory
    if not os.path.isdir(result_dir):
        os.mkdir(result_dir)

    # counts.saveAsTextFile("{}/{}".format(result_dir, name))

    # Save dataframe to disk (or do something with it)
    df_result.toPandas().to_csv("{}/{}".format(result_dir, name), index=False)

    return df_result


if __name__ == "__main__":
    file_path = sys.argv[1]
    path = file_path.split("/")
    file_name = path[1]
    """
    files = [
        (folder_path + "/2h6a75nk", "2h6a75nk"),
        (folder_path + "/4vxdw3pa", "4vxdw3pa"),
        (folder_path + "/datumz6m", "datumz6m"),
        (folder_path + "/dybs9bnk", "dybs9bnk"),
        (folder_path + "/j4j4xdw6", "j4j4xdw6"),
        (folder_path + "/kh9excea", "kh9excea"),
        (folder_path + "/vwvram8", "vwvram8"),
        (folder_path + "/weh83uyn", "weh83uyn"),
        (folder_path + "/ym8s5fm4", "ym8s5fm4")
    ]"""
    generate_word_count(file_path, file_name)