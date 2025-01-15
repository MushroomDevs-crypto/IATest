import tweepy
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Substitua pelos seus dados de autenticação
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Autenticação
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Cria a API
api = tweepy.API(auth, wait_on_rate_limit=True)

# Função para responder a menções
def reply_to_mentions():
    # Obtém os últimos 20 tweets onde o bot foi mencionado
    mentions = api.mentions_timeline(count=20, tweet_mode="extended")

    for mention in mentions:
        try:
            print(f"Respondendo a: {mention.user.screen_name} - {mention.full_text}")
            
            # Evita responder a menções já tratadas
            if mention.favorited:
                continue

            # Responde ao tweet com "Hello World!"
            api.update_status(
                status=f"@{mention.user.screen_name} Hello World!",
                in_reply_to_status_id=mention.id
            )

            # Marca o tweet como favorito para evitar duplicação de respostas
            api.create_favorite(mention.id)
            print(f"Respondido com sucesso a {mention.user.screen_name}")

        except Exception as e:
            print(f"Erro ao responder a {mention.user.screen_name}: {e}")

# Executa a função para responder às menções
if __name__ == "__main__":
    print("Bot iniciado. Respondendo às menções...")
    reply_to_mentions()
    print("Execução concluída.")

