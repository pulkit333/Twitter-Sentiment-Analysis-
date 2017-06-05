# 6wKJr725XvdUjF6wqlmvykp3c
# BQngc5teAtkcuAWQBjAGpuwsBuYphapj0PhiCH6kOtQHT9YwNm
# 1050784424-9JlNKl4u6qnlH398eJSWSoWsChnpclYQKeJbJOy
# djwX0DGWfG91H0gPdxRbVY3PEt9cYWkGmheb6R5RKgGUf

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sentiment_modJ as s
import json
import re

ckey = '6wKJr725XvdUjF6wqlmvykp3c'
csecret = 'BQngc5teAtkcuAWQBjAGpuwsBuYphapj0PhiCH6kOtQHT9YwNm'
atoken = '1050784424-9JlNKl4u6qnlH398eJSWSoWsChnpclYQKeJbJOy'
asecret = 'djwX0DGWfG91H0gPdxRbVY3PEt9cYWkGmheb6R5RKgGUf'


class listener(StreamListener):
    def on_data(self, data):

        try:
            all_data = json.loads(data)
            tweet = str(all_data["text"])

            url = re.findall("(https?://[^\s]+)", tweet)
            for i in url:
                tweet = tweet.replace(i, "")

            url = re.findall("(@.+?(?:\s+|$))", tweet)
            for i in url:
                tweet = tweet.replace(i, "")

            url = re.findall("(&.*?;)", tweet)
            for i in url:
                tweet = tweet.replace(i, "")

            url = re.findall("(!+?!)", tweet)
            for i in url:
                tweet = tweet.replace(i, "")
            url = re.findall("(\.+?\.)", tweet)
            for i in url:
                tweet = tweet.replace(i, " ")

            tweet = tweet.replace("RT", "", 1)
            tweet = re.sub(r"[^\w\.\?']", ' ', tweet)
            tweet = tweet.strip()
            sentiment, conf = s.sentiment(tweet)
            print(tweet, "======>", sentiment, "======>", conf)
            print("=================================================================")
            if conf >= .5:
                output = open("twitter-out.txt", "a")
                output.write(sentiment)
                output.write("\n")
                output.close()
        except KeyError:
            pass
        except UnicodeEncodeError:
            pass
        return True

    def on_error(self, status):
        print(status)


auth1 = OAuthHandler(ckey, csecret)

auth1.set_access_token(atoken, asecret)
ourStream = Stream(auth1, listener())
words = input("Input a Word or Words to track separated by a Space:")
word_list = [w for w in words.split(" ")]
ourStream.filter(track=word_list)
