import csv
import os
import pandas as pd
import tweet_extract
import text_pre_processor
import emotion_analysis
import emotion_analysis_2

# one trace for each emotion

users = ['pulvereyes', 'wkulhanek', 'TheDemocrats', 'GOP']


# [c1,v1,a1,d1]
# [c2,v1,a1,d1]
# [c3,v1,a1,d1]
# [c4,v1,a1,d1]
# [c5,v1,a1,d1]
# [c6,v1,a1,d1]
# [c7,v1,a1,d1]
# [c8,v1,a1,d1]


def process_csv():
    for user in users:
        with open("output_" + user + ".csv", 'r') as fin, \
                open("new_output_" + user + ".csv", "w", newline='') as fout:
            reader = csv.reader(fin, delimiter=',')
            writer = csv.writer(fout)
            writer.writerow(['DateTime', 'Original Tweet', 'Processed Tweet', 'Emotion', 'anger', 'fear', 'anticipation', 'surprise', 'joy', 'sadness', 'trust', 'disgust', 'keywords', 'keyword_counts'])
            for row in reader:
                vals = row[3][1:].split(',')
                row.append(vals[0])
                row.append(vals[4])
                row.append(vals[8])
                row.append(vals[12])
                row.append(vals[16])
                row.append(vals[20])
                row.append(vals[24])
                row.append(vals[28])
                important = []
                row.append(important)
                row.append(len(important))
                writer.writerow(row)
            fin.close()
            fout.close()
        os.remove("output_" + user + ".csv")


if __name__ == "__main__":
    tweet_extract.extract_tweets()
    print('finished extracting original users')
    tweet_extract.extract_tweets_politics()
    print('finished politics')
    text_pre_processor.process()
    print('finished pre process')
    emotion_analysis_2.get_category_score()
    print('got scores')
    process_csv()
    print('done processing csv')
