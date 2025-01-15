import tweepy
import os
from time import sleep
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Credenciais da API do X (Twitter)
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Autenticação com a API v2
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    wait_on_rate_limit=True,
)

# Função para obter o ID do usuário autenticado
def get_user_id():
    try:
        user = client.get_user(username="@Mushroomdevs")  # Substitua YOUR_USERNAME pelo nome de usuário do bot
        return user.data.id
    except Exception as e:
        print(f"Erro ao obter ID do usuário: {e}")
        return None

# Função para responder a menções
def reply_to_mentions(last_mention_id=None):
    user_id = get_user_id()
    if not user_id:
        print("Não foi possível obter o ID do usuário.")
        return

    try:
        # Busca menções ao bot desde o último ID processado
        mentions = client.get_users_mentions(
            id=user_id,
            since_id=last_mention_id,
            max_results=20,
            tweet_fields=["id", "author_id"],
        )
        
        if mentions.data:
            print(f"Encontradas {len(mentions.data)} menções.")
            for mention in mentions.data:
                print(f"Respondendo ao tweet {mention.id}...")
                client.create_tweet(
                    text="Hello World!", in_reply_to_tweet_id=mention.id
                )
                last_mention_id = mention.id  # Atualiza o ID da última menção respondida
        else:
            print("Nenhuma menção nova encontrada.")
    except tweepy.errors.TweepyException as e:
        print(f"Erro ao buscar ou responder menções: {e}")

# Loop para rodar continuamente
if __name__ == "__main__":
    last_id = None
    while True:
        print("Verificando menções...")
        reply_to_mentions(last_id)
        print("Aguardando 2 minutos antes da próxima verificação...")
        sleep(120)  # Aguarda 2 minutos para evitar atingir os limites da API


