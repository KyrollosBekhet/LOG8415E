import os
import urllib.request
import time


def run_word_count(path, name, try_number):
    start = time.time()
    split = path.split("/")
    os.system("hadoop jar wordcount.jar org.myorg.WordCount {0}/{1} output_{1}_{2}"
              .format(split[0], name, try_number))
    end = time.time()
    return end - start


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


def main():
    os.system("javac -d wordcount_classes WordCount.java")
    os.system("jar -cvf wordcount.jar -C wordcount_classes/ .")

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

    template_text = "the time required to analyze {} is {} \n"
    final_text = ""
    for i in range(0, 3):
        for path, name in files:
            time = run_word_count(path, name, i)
            final_text += template_text.format(name, time)

    print(final_text)
