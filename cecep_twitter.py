import tweepy
import pandas as pd

# Twitter API credentials
API_KEY = " oyrpA2bAY4rxCDelwbGpmUosy"
API_SECRET_KEY = "ptTlVcNwNCFFf376zU9N4Sr3xhEpVD5RGCZAx3WYCuybBUu914"
ACCESS_TOKEN = "1813762786532741120-Oauh4i8jlnMeo5VBikrWvl2sNenvdI"
ACCESS_TOKEN_SECRET = "Dwsrs51WTtZit7nVglshv9S7ldYjEL5hdhb4wbgrE7V5s"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIlnvwEAAAAABkIiP8DbNcBOjbugW%2BN1%2B6V0daI%3DjOO9LoPN3n8wWMKdjDqeph5u1SzFdAnfFa3dHUyEd8VcmzFh0l"


# client = tweepy.Client(
#     consumer_key=API_KEY,
#     consumer_secret=API_SECRET_KEY,
#     access_token=ACCESS_TOKEN,
#     access_token_secret=ACCESS_TOKEN_SECRET
# )
# Authenticate with Twitter API v2 and OAuth 1.0a
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Twitter handle you want to scrape
username = "madatcommunity"

# Fetch the user object by username
user = client.get_user(username=username)
user_id = user.data.id

# Fetch tweets from the user's timeline (up to 100 tweets per request)
tweets = client.get_users_tweets(id=user_id, max_results=100)

tweets_data = []

# Process the fetched tweets
for tweet in tweets.data:
    tweet_text = tweet.text
    tweet_date = tweet.created_at

    tweets_data.append((tweet_text, tweet_date))

    print(f"Date: {tweet_date}, Tweet: {tweet_text}")

# Create a DataFrame and save it to an Excel file
df = pd.DataFrame(tweets_data, columns=["Tweet", "Date"])
df.to_excel("tweets.xlsx", index=False)

print(f"Total tweets collected: {len(tweets_data)}")