from redis_model import *

import json
from datetime import datetime

def process_json_file(filename):
    # Read JSON file
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                tweet = json.loads(line)
                process_tweet(tweet)

def process_tweet(tweet):
    # Extract user info
    user_info = tweet.get('user', {})
    username = user_info.get('screen_name')
    
    # Skip if no username
    if not username:
        return
    
    # Create user if not exists
    if not r.exists(username):
        add_user(username)
    
    # Update followers/following counts
    followers = user_info.get('followers_count', 0)
    following = user_info.get('friends_count', 0)
    
    update_user_followers(username, followers)
    update_user_following(username, following)
    
    # Increment chirps count
    increment_user_chirps(username)
    
    # Add chirp to timeline
    timestamp = int(tweet.get('timestamp_ms', 0)) // 1000  # Convert to seconds
    chirp_content = tweet.get('text', '')
    
    if timestamp and chirp_content:
        add_chirps(timestamp, chirp_content)


# Execute processing
process_json_file('/home/lchristen/CHIRP_lab/data/00.json')