import GetOldTweets3 as got
import datetime
import csv

#id = 14874721
#username = pulvereyes
#id = 14396017
#username = wkulhanek
#start date: 2012.9.4
#end date: 2013.8.1


set_of_users = ['pulvereyes', 'wkulhanek']
start_date = "2012-09-04"
end_date = "2013-08-01"
set_of_users_politics = ['TheDemocrats', 'GOP']
start_date_politics = "2013-01-01"
end_date_politics = "2013-02-01"


def extract_tweets():
    for user in set_of_users:
        tweetCriteria = got.manager.TweetCriteria().setUsername(user).setSince(start_date).setUntil(end_date)
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        user_tweets = [[tweet.date, tweet.text] for tweet in tweets]
        with open('output_'+user+'.csv', 'w+', newline='') as file:
            writer = csv.writer(file)
            for tweet in user_tweets:
                writer.writerow(tweet)
            file.close()


def extract_tweets_politics():
    for user in set_of_users_politics:
        tweetCriteria = got.manager.TweetCriteria().setUsername(user).setSince(start_date_politics).setUntil(end_date_politics)
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        user_tweets = [[tweet.date, tweet.text] for tweet in tweets]
        with open('output_'+user+'.csv', 'w+', newline='') as file:
            writer = csv.writer(file)
            for tweet in user_tweets:
                writer.writerow(tweet)
            file.close()


def extract_tweet_1():
    tweetCriteria = got.manager.TweetCriteria().setUsername("pulvereyes").setSince("2012-09-04").setUntil("2013-08-01")
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    user_tweets = [[tweet.date, tweet.text] for tweet in tweets]
    with open('output_got.csv', 'w+', newline='') as file:
        writer = csv.writer(file)
        for tweet in user_tweets:
            writer.writerow(tweet)
        file.close()


def extract_tweet_2():
    #username2 =realDonaldTrump
    tweetCriteria2 = got.manager.TweetCriteria().setUsername("wkulhanek").setSince("2012-09-04").setUntil("2013-08-01")
    tweets2 = got.manager.TweetManager.getTweets(tweetCriteria2)
    user_tweets2 = [[tweet.date, tweet.text] for tweet in tweets2]
    with open('output2_got.csv', 'w+', newline='') as file2:
        writer2 = csv.writer(file2)
        for tweet in user_tweets2:
            writer2.writerow(tweet)
        file2.close()


if __name__ == "__main__":
    extract_tweets()
    extract_tweets_politics()
    # extract_tweet_1()
    # extract_tweet_2()
