import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum
import os
import urllib.request
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


def acquire_datasets(urls, dest_dir="text_datasets"):
    filenames = []

    # Create data destination directory
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    for i, url in enumerate(urls):

        filename = "text_{}".format(i)
        filepath = "{}/{}".format(dest_dir, filename)

        filenames.append((filepath, filename))

        file = open(filepath, 'wb')

        with urllib.request.urlopen(url) as response:
            data = response.read()
            file.write(data)

        file.close()  

    return filenames

if __name__ == "__main__":
    # Datasets given in the assigment description
    urls = ['https://tinyurl.com/4vxdw3pa',
            'https://tinyurl.com/kh9excea',
            'https://tinyurl.com/dybs9bnk',
            'https://tinyurl.com/datumz6m',
            'https://tinyurl.com/j4j4xdw6',
            'https://tinyurl.com/ym8s5fm4',
            'https://tinyurl.com/2h6a75nk',
            'https://tinyurl.com/vwvram8',
            'https://tinyurl.com/weh83uyn'
            ]

    files = acquire_datasets(urls)
    
    for path, name in files:
        generate_word_count(os.path.abspath(path), name)