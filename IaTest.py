import tweepy
import os
import sys

# Set up API credentials from environment variables
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Validate credentials
if not all([api_key, api_secret, access_token, access_token_secret, bearer_token]):
    print("Error: Missing Twitter API credentials. Please check your environment variables.")
    sys.exit(1)

try:
    # Set up Twitter client
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
        wait_on_rate_limit=True
    )

    # Verify credentials
    client.get_me()
except tweepy.errors.Unauthorized:
    print("Error: Invalid credentials. Please check your Twitter API keys and tokens.")
    print("Make sure you have created a project in the Twitter Developer Portal.")
    sys.exit(1)
except Exception as e:
    print(f"Error during authentication: {e}")
    sys.exit(1)


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




