import tweepy
from datetime import datetime, timedelta
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import schedule
import time
import os

# Helpful when testing locally
from dotenv import load_dotenv
load_dotenv()

# Load API keys from environment variables
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "YourKey")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "YourKey") 
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "YourKey")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "YourKey")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "YourKey")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YourKey")

class TwitterBot:
    def __init__(self):
        self.twitter_api = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )
        self.llm = ChatOpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")
        self.me_id = self.twitter_api.get_me()[0].id
        self.processed_mentions = set()  # Store processed mention IDs in memory

    def generate_response(self, tweet_text):
        system_template = """
        You are a witty and sarcastic tech enthusiast who loves to make predictions about the future.
        Your responses should be:
        - Humorous but insightful
        - Limited to 240 characters
        - Include at least one tech-related reference
        - End with a bold prediction
        
        If you can't make a prediction, respond with "My crystal ball needs debugging 🔧"
        """
        
        human_template = "{text}"
        
        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(human_template)
        ])
        
        messages = chat_prompt.format_prompt(text=tweet_text).to_messages()
        response = self.llm(messages).content
        return response

    def handle_mentions(self):
        # Get mentions from last hour
        start_time = datetime.utcnow() - timedelta(hours=1)
        mentions = self.twitter_api.get_users_mentions(
            id=self.me_id,
            start_time=start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            tweet_fields=['created_at']
        ).data

        print(f"Mentions retrieved: {mentions.data if mentions else 'None'}")

        if not mentions:
            return

        for mention in mentions:
            # Check if we've already processed this mention
            if mention.id not in self.processed_mentions:
                try:
                    response = self.generate_response(mention.text)
                    print(f"Generated response: {response}")
                    self.twitter_api.create_tweet(
                        text=response,
                        in_reply_to_tweet_id=mention.id
                    )
                    print(f"Successfully replied to mention {mention.id}")
                    # Add to processed mentions
                    self.processed_mentions.add(mention.id)
                    
                except Exception as e:
                    print(f"Error handling mention {mention.id}: {str(e)}")

def main():
    bot = TwitterBot()
    schedule.every(5).minutes.do(bot.handle_mentions)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()

