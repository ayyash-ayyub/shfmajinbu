import csv
import snscrape.modules.twitter as sntwitter


# Function to scrape tweets
def scrape_twitter(username, keyword_search, hashtags, max_results=20):
    # Query to search for tweets from the user, containing keywords and hashtags
    query = f'from:{username} {keyword_search} ' + ' '.join(hashtags)

    # List to store scraped data
    tweet_data = []
    
    # Scraping tweets
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_results:
            break
        tweet_data.append({
            'Username': tweet.user.username,
            'Tweet': tweet.content,
            'Date': tweet.date,
            'Likes': tweet.likeCount,
            'Retweets': tweet.retweetCount,
        })

    # Save to CSV
    with open(f'{username}_tweets.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Username', 'Tweet', 'Date', 'Likes', 'Retweets']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in tweet_data:
            writer.writerow(data)

    print(f"Successfully saved {len(tweet_data)} tweets to {username}_tweets.csv")

# Customize the parameters
username = 'DailyDarkWeb'
keyword_search = 'CyberAttack'
hashtags = ['#CyberAttack', '#Ransomware']

# Call the scraping function
scrape_twitter(username, keyword_search, hashtags)
