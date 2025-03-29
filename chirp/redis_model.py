import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

MAX_TOPS_ITEMS = 5

# CHIRP FUNCTIONS

def add_chirps(timestamp, username, chirp_content):
    # Add chirp content to Redis zset with timestamp as score.
    chirp_content = username + ': ' + chirp_content
    r.zadd('chirps', {chirp_content: timestamp})
    # can't have more than 5 items in the list
    if r.zcard('chirps') > MAX_TOPS_ITEMS:
        # remove the oldest item
        r.zremrangebyrank('chirps', 0, 0)

def get_chirps():
    # Get all chirps from Redis zset.
    chirps = r.zrevrange('chirps', 0, -1, withscores=True)
    return [(chirp, int(score)) for chirp, score in chirps]


# USER FUNCTIONS

def add_user(username):
    # Add user to Redis hashset
    r.hset(username, mapping={
        'chirps': 0,
        'followers': 0,
        'following': 0
    })

def increment_user_chirps(username):
    # Get current chirp count
    current = int(r.hget(username, 'chirps') or 0)
    new_count = current + 1
    r.hset(username, 'chirps', new_count)
    # Update best chirpers
    best_chirpers = r.zrevrange('best_chirpers', 0, -1, withscores=True)
    if len(best_chirpers) < MAX_TOPS_ITEMS or new_count > int(best_chirpers[-1][1]):
        r.zadd('best_chirpers', {username: new_count})
        if r.zcard('best_chirpers') > MAX_TOPS_ITEMS:
            r.zremrangebyrank('best_chirpers', 0, 0)

def update_user_following(username, n):
    r.hset(username, 'following', n)

def update_user_followers(username, n):
    r.hset(username, 'followers', n)
    # check if n > last element of user with most followers if so, add user to most_followers
    most_followers = r.zrevrange('most_followers', 0, -1, withscores=True)
    if len(most_followers) < MAX_TOPS_ITEMS or n > int(most_followers[-1][1]):
        # add user to most_followers
        r.zadd('most_followers', {username: n})
        # remove the oldest item
        if r.zcard('most_followers') > MAX_TOPS_ITEMS:
            r.zremrangebyrank('most_followers', 0, 0)

def get_user(username):
    # Get user from Redis hashset
    user = r.hgetall(username)
    return {k: int(v) for k, v in user.items()}


# LEADERBOARD FUNCTIONS

def get_top_chirpers():
    # Get top chirpers from Redis zset.
    chirpers = r.zrevrange('best_chirpers', 0, MAX_TOPS_ITEMS - 1, withscores=True)
    return [(chirper, int(score)) for chirper, score in chirpers]

def get_top_followers():
    # Get most followers from Redis zset.
    most_followers = r.zrevrange('most_followers', 0, MAX_TOPS_ITEMS - 1, withscores=True)
    return [(follower, int(score)) for follower, score in most_followers]