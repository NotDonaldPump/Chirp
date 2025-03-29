import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

MAX_TOPS_ITEMS = 5

def add_chirps(timestamp, chirp_content):
    # Add chirp content to Redis zset with timestamp as score.
    r.zadd('chirps', {chirp_content: timestamp})

    # can't have more than 5 items in the list
    if r.zcard('chirps') > MAX_TOPS_ITEMS:
        # remove the oldest item
        r.zremrangebyrank('chirps', 0, 0)

def get_chirps():
    # Get all chirps from Redis zset.
    chirps = r.zrevrange('chirps', 0, -1, withscores=True)
    # Convert scores to integers and return as a list of tuples.
    return [(chirp, int(score)) for chirp, score in chirps]

def get_top_chirpers():
    # Get top chirpers from Redis zset.
    chirpers = r.zrevrange('best_chirpers', 0, MAX_TOPS_ITEMS - 1, withscores=True)
    # Convert scores to integers and return as a list of tuples.
    return [(chirper.decode('utf-8'), int(score)) for chirper, score in chirpers]

def add_user(username):
    # Add user to Redis hashset
    """
    user = {
        'chirps': 0,
        'followers': 0,
        'following': 0
    }
    """
    r.hset(username, mapping={
        'chirps': 0,
        'followers': 0,
        'following': 0
    })

def update_user_chirps(username, n):
    r.hset(username, 'chirps', n)

    # check if n > last element of best_chirpers
    # if so, add user to best_chirpers
    best_chirpers = r.zrevrange('best_chirpers', 0, -1, withscores=True)
    if len(best_chirpers) < MAX_TOPS_ITEMS or n > int(best_chirpers[-1][1]):
        # add user to best_chirpers
        r.zadd('best_chirpers', {username: n})

        # remove the oldest item
        if r.zcard('best_chirpers') > MAX_TOPS_ITEMS:
            r.zremrangebyrank('best_chirpers', 0, 0)

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

    # check if n > last element of user with most followers
    # if so, add user to most_followers
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
    # Convert values to integers and return as a dictionary.
    return {k.decode('utf-8'): int(v) for k, v in user.items()}


def get_most_followers():
    # Get most followers from Redis zset.
    most_followers = r.zrevrange('most_followers', 0, MAX_TOPS_ITEMS - 1, withscores=True)
    # Convert scores to integers and return as a list of tuples.
    return [(follower.decode('utf-8'), int(score)) for follower, score in most_followers]