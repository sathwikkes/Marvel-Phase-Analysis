## special thanks to the creator of the nitter scraper: https://pypi.org/project/ntscraper/
import pandas as pd 
from ntscraper import Nitter
import time


# scraper = Nitter()
# search_term = "LosAngelesLakers"
# tweets = scraper.get_tweets(search_term, mode='term', number = 5)
# data = []
# for tweet in tweets["tweets"]: 
#     print(tweet)
    # print("--------Next Tweet--------")
    # tweet_data = [tweet["link"], tweet["text"], tweet["date"], tweet['stats']["comments"], tweet['stats']["likes"], tweet['stats']["retweets"]]
    # data.append(tweet_data)

# df = pd.DataFrame(data, columns = ["Link", "Text", "Date", "Comments", "Likes", "Retweets"])
# print(df.head())



def get_tweets(name,modes,num):
  #  scraper = Nitter(instance="https://nitter.net")  # a less-used instance
    scraper = Nitter()
    tweets = scraper.get_tweets(name, mode=modes, number = num)
    data = []
    for tweet in tweets["tweets"]:
        tweet_data = [
            tweet["link"], 
            tweet["text"], 
            tweet["date"], 
            tweet['stats']["comments"], 
            tweet['stats']["likes"], 
            tweet['stats']["retweets"]
        ]
        data.append(tweet_data)
    df = pd.DataFrame(data, columns = ["Link", "Text", "Date", "Comments", "Likes", "Retweets"])
    df.to_csv(name + ".csv", index = False)
    return df 


def get_tweets_with_retries(name, modes, num, max_retries=3):
    for _ in range(max_retries):
        try:
            return get_tweets(name, modes, num)
        except Exception as e:
            if "rate limited" in str(e):
                print(f"Rate limited. Retrying in {60} seconds...")
                time.sleep(60)
    raise Exception("Failed to fetch tweets after retries.")

print(get_tweets("Guardians of the Galaxy", "term", 100))


