import requests

# Your credentials
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIlnvwEAAAAAepyHpwAs7h7XlffPJeK0D%2F6k3d8%3DmGLXnhhmmcxbyrsiWbvVydPcRRsPGyqxvCJbdwO03UJFwLCeyo"

# Function to create headers for authentication
def create_headers(bearer_token):
    return {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2TweetLookupPython"
    }

# Function to get user ID from username
def get_user_id(username, bearer_token):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    response = requests.get(url, headers=create_headers(bearer_token))
    if response.status_code == 200:
        return response.json()['data']['id']
    else:
        raise Exception(f"Error fetching user ID: {response.status_code} - {response.text}")

# Function to get tweets from user ID
def get_user_tweets(user_id, bearer_token, max_results=10):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "max_results": max_results
    }
    response = requests.get(url, headers=create_headers(bearer_token), params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"Error fetching tweets: {response.status_code} - {response.text}")

# Main function to fetch and display tweets
def main(username):
    try:
        user_id = get_user_id(username, BEARER_TOKEN)
        tweets = get_user_tweets(user_id, BEARER_TOKEN)
        if tweets:
            for tweet in tweets:
                print(f"Tweet ID: {tweet['id']} - Tweet Text: {tweet['text']}")
        else:
            print("No tweets found for this user.")
    except Exception as e:
        print(str(e))

# Replace 'H4ckManac' with the desired Twitter username
main("H4ckManac")
