import tweepy
import csv

# Twitter API credentials
bearer_token = "AAAAAAAAAAAAAAAAAAAAACpmvwEAAAAAPxbU9NDfrjIQSYxMQ9wjOdqJvJI%3DipkNQF7HakFDugoUg5kLAdYrwo7SDRGY8h7KOPFyErOBgxcrVl"
api_key = "jihSHPsw5X7YS8yVPpJX16SFk"
api_key_secret = "ZUrPsoC3eIo6qSnKJjA6kDwe6hsvwAm3k2IGtYPBi9IwF7NVG6"
access_token = "205080697-P6OhcPTPy4ORaCIFdcB01ZHubPaApJLWTgDgXs89"
access_token_secret = "Dwsrs51WTtZit7nVglshv9S7ldYjEL5hdhb4wbgrE7V5s"

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)

client = tweepy.Client(bearer_token=bearer_token, 
                       consumer_key=api_key, 
                       consumer_secret=api_key_secret, 
                       access_token=access_token, 
                       access_token_secret=access_token_secret)

# Usernames and hashtags
usernames = ['FalconFeeds.io', 'H4ckManac', 'DailyDarkWeb']
hashtags = '#CyberAttack #Ransomware'

# Function to retrieve tweets
def retrieve_tweets(username, hashtag):
    query = f'from:{username} {hashtag}'
    tweets = client.search_recent_tweets(query=query, tweet_fields=['created_at', 'text'])
    return tweets.data if tweets.data else []

# Collect tweets
all_tweets = []
for username in usernames:
    for hashtag in hashtags.split(' '):
        tweets = retrieve_tweets(username, hashtag)
        for tweet in tweets:
            all_tweets.append({
                'Username': username,
                'Tweet': tweet.text,
                'Created At': tweet.created_at
            })

# Save to CSV
csv_file = 'tweetsjadi.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Username', 'Tweet', 'Created At'])
    writer.writeheader()
    for tweet in all_tweets:
        writer.writerow(tweet)

print(f"Tweets saved to {csv_file}")
