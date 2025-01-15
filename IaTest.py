import tweepy
import os

# Set up API credentials from environment variables
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Set up Twitter client
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Set up OAuth1 authentication for API v1.1
auth = tweepy.OAuth1UserHandler(
    api_key, api_secret, access_token, access_token_secret
)
api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        try:
            # Get the tweet that mentioned the bot
            mentioned_tweet = client.get_tweet(tweet.id)
            
            # Reply to the tweet
            client.create_tweet(
                text="Hello World",
                in_reply_to_tweet_id=tweet.id
            )
        except Exception as e:
            print(f"Error: {e}")

# Initialize stream
stream = MyStreamListener(bearer_token)

# Add rule to track mentions
# Replace USERNAME with your bot's username
stream.add_rules(tweepy.StreamRule("@Mushroomdevs"))

# Start streaming
stream.filter()




