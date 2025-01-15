import tweepy
import time

# Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)

# Create Client for v2 endpoints
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

class MyStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        try:
            # Get the tweet that mentioned the bot
            tweet_data = client.get_tweet(
                tweet.id,
                expansions=['referenced_tweets']
            )
            
            # If this tweet is a reply or quote
            if tweet_data.data.referenced_tweets:
                # Get the original tweet that was replied to or quoted
                original_tweet_id = tweet_data.data.referenced_tweets[0].id
                
                # Reply to the original tweet
                client.create_tweet(
                    text="hello world",
                    in_reply_to_tweet_id=original_tweet_id
                )
        except Exception as e:
            print(f"Error: {e}")

# Initialize stream
stream = MyStreamListener(bearer_token="YOUR_BEARER_TOKEN")

# Get bot's user ID
bot_user = client.get_me()
bot_id = bot_user.data.id

# Add rule to track mentions
stream.add_rules(tweepy.StreamRule(f"@{bot_user.data.username}"))

# Start streaming
print("Starting stream...")
stream.filter()



