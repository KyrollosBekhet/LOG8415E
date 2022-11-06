import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum
import os

def generate_word_count(path, name, result_dir="results"):
    spark = SparkSession.builder.getOrCreate()

    # Create a DataFrame from the text file
    text_file = spark.sparkContext.textFile(path)


    # Run WordCount pipeline from https://spark.apache.org/examples.html
    counts = text_file.flatMap(lambda line: line.split(" ")) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)


    # Convert pipeline back to DataFrame
    df_result = counts.toDF(["word", "count"])

    word_count = df_result.select(_sum('count')).alias('word_count').collect()[0][0]


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
    generate_word_count(file_path, file_name)