from redis_model import *
import json
import os
from datetime import datetime

def process_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                tweet = json.loads(line)
                process_tweet(tweet)

def process_tweet(tweet):
    user_info = tweet.get('user', {})
    username = user_info.get('screen_name')
    
    if not username:
        return
    
    if not r.exists(username):
        add_user(username)
    
    followers = user_info.get('followers_count', 0)
    following = user_info.get('friends_count', 0)
    
    update_user_followers(username, followers)
    update_user_following(username, following)
    increment_user_chirps(username)

    timestamp = int(tweet.get('timestamp_ms', 0))
    chirp_content = tweet.get('text', '')
    
    if timestamp and chirp_content:
        add_chirps(timestamp, username, chirp_content)

data_dir = os.path.join(os.path.dirname(__file__), '../data')

for filename in sorted(os.listdir(data_dir)):
    if filename.endswith('.json'):
        filepath = os.path.join(data_dir, filename)
        print(f"Processing {filename}...")
        process_json_file(filepath)
print("All files processed.")