import csv
import datetime
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from gensim.summarization import keywords
from rake_nltk import Rake
import nltk
import pandas as pd
nltk.download('stopwords')

emotion_categories = ['anger', 'fear', 'anticipation', 'surprise', 'joy', 'sadness', 'trust', 'disgust']
def find_mood(input_date, user):
    file = 'new_output_' + user + '_words.csv'
    category_list = [0 for _ in range(8)]
    category_num = 0
    mood = []
    csv_data = pd.read_csv(file)
    for row in csv_data.itertuples():
        time = datetime.datetime.strptime(input_date, '%Y-%m-%d')
        word_time = datetime.datetime.strptime(getattr(row, 'DateTime')[0:10], '%Y-%m-%d')
        if abs(word_time.__sub__(time).days) < 7:
            emotions = getattr(row, 'Categories')[1:len(getattr(row, 'Categories')) - 1].split(",")
            emotions[0] = emotions[0][1:len(emotions[0]) - 1]
            for j in range(1, len(emotions)):
                emotions[j] = emotions[j][2:len(emotions[j]) - 1]
            for emotion in emotions:
                category_num += 1
                position = emotion_categories.index(emotion)
                category_list[position] += 1
    for i in range(0, 8):
        if int(category_num) == 0:
            continue
        if float(category_list[i]) / float(category_num) >= 0.125:
            # print(emotion_categories[i])
            mood.append(emotion_categories[i])
            # print(float(category_list[i]) / float(category_num))
    return mood


def word_cloud(input_date, user):
    file = 'new_output_' + user + '_words.csv'
    string = ''
    csv_data = pd.read_csv(file)
    for row in csv_data.itertuples():
        time = datetime.datetime.strptime(input_date, '%Y-%m-%d')
        word_time = datetime.datetime.strptime(getattr(row, 'DateTime')[0:10], '%Y-%m-%d')
        if abs(word_time.__sub__(time).days) < 7:
            string += ' '
            string += getattr(row, 'Word')
    wc = WordCloud(
        background_color='white', width=400, height=400, margin=2).generate(string)
    return wc.to_image()


def find_keywords(input_date, user):
    file = 'new_output_' + user + '.csv'
    corpus = ''
    with open(file, 'r') as fin:
        reader = csv.reader(fin, delimiter=',')
        for row in reader:
            if row[0] == 'DateTime':
                continue
            time = datetime.datetime.strptime(input_date, '%Y-%m-%d')
            row[0] = datetime.datetime.strptime(row[0][0:10], '%Y-%m-%d')
            if abs(row[0].__sub__(time).days) < 7:
                corpus += ' '
                corpus += row[1]
    # print (corpus)
    keyword_list = keywords(corpus, words=None, split=True, scores=False, pos_filter=('NN', 'JJ'), lemmatize=True,
                            deacc=True)
    # print(keyword_list)
    # Get the VAD value and the emotion categories of each keyword
    result_dict = dict()
    file_name = 'new_output_' + user + '_words.csv'
    with open(file_name, 'r') as fin:
        reader = csv.reader(fin, delimiter=',')
        for row in reader:
            if row[4] == 'DateTime':
                continue
            if len(result_dict) > 10:
                break
            time = datetime.datetime.strptime(input_date, '%Y-%m-%d')
            row[4] = datetime.datetime.strptime(row[4][0:10], '%Y-%m-%d')
            if abs(row[4].__sub__(time).days) < 7:
                if row[0] in keyword_list:
                    if row[0] not in result_dict.keys():
                        result_dict[row[0]] = list()
                        row[5] = row[5][1:len(row[5]) - 1]
                        emotions = row[5].split(",")
                        emotions[0] = emotions[0][1:len(emotions[0]) - 1]
                        for j in range(1, len(emotions)):
                            emotions[j] = emotions[j][2:len(emotions[j]) - 1]
                        result_dict[row[0]].append(emotions)
                        result_dict[row[0]].append(float(row[1]))
                        result_dict[row[0]].append(float(row[2]))
                        result_dict[row[0]].append(float(row[3]))
    # print(result_dict.keys())
    return result_dict


if __name__ == "__main__":
    # find_mood("2016-12-07")
    # word_cloud("2016-10-09")
    find_keywords("2016-12-07", "14874721")


