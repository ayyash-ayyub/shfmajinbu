import subprocess
import csv
import os


filename_prefix = 'tweets_'
filtered_filename = 'tweets_filtered.csv'
hashtags = '#CyberAttack #Ransomware'
limit = 100
twitter_auth_token = '33d247556507cf5d685d56eff99a5d1739e413af'
target_users = ['DailyDarkWeb','FalconFeeds.io', 'H4ckManac']

def run_tweet_harvest(search_query, user):
    temp_filename = f'{filename_prefix}{user.replace(" ", "_")}.csv'
    
    command = [
        'npx', '--yes', 'tweet-harvest@2.6.1',
        '-o', temp_filename,
        '-s', search_query,
        '-l', str(limit),
        '--token', twitter_auth_token
    ]
    
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    
    if result.returncode != 0:
        print(f"Error running tweet-harvest for {user}:")
        print(result.stderr)
        return None
    
    print(f'Successfully saved tweets from {user} to {temp_filename}')
    return temp_filename

def filter_tweets_by_hashtags(input_filenames, output_filename, hashtags):
    hashtag_set = set(hashtags.lower().split())
    processed_files = set()
    found_any = False
    
    with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        header_written = False
        
        for filename in input_filenames:
            if not os.path.isfile(filename):
                print(f"File {filename} does not exist, skipping.")
                continue

            with open(filename, mode='r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                if not header_written:
                    # Write header once
                    fieldnames = reader.fieldnames
                    writer.writerow(fieldnames)
                    header_written = True
                
                for row in reader:
                    tweet_text = row.get('text', '').lower()
                    tweet_hashtags = set(part for part in tweet_text.split() if part.startswith('#'))
                    
                    # Check if any of the hashtags are present
                    if hashtag_set.intersection(tweet_hashtags):
                        found_any = True
                        writer.writerow(row)
        
        if not found_any:
            print('No tweets containing the hashtags were found.')
    
    
    for file in processed_files:
        os.remove(file)

def get_tweets_from_users():
    input_filenames = []
    
    for user in target_users:
        
        search_query = f'from:{user} lang:en'
        temp_filename = run_tweet_harvest(search_query, user)
        if temp_filename:
            input_filenames.append(temp_filename)
    
    
    if input_filenames:
        filter_tweets_by_hashtags(input_filenames, filtered_filename, hashtags)
    else:
        print('No tweets were fetched.')

if __name__ == "__main__":
    get_tweets_from_users()
