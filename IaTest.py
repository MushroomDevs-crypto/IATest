import tweepy
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Substitua pelos seus dados de autenticação
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Cria o cliente com a API v2
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    wait_on_rate_limit=True,
)

# Função para responder a menções
def reply_to_mentions():
    # Obtém o ID do usuário autenticado
    user = client.get_me().data
    user_id = user.id

    # Obtém as últimas 20 menções
    mentions = client.get_users_mentions(user_id, max_results=20)

    if mentions.data:
        for mention in mentions.data:
            try:
                print(f"Respondendo a: {mention.text}")

                # Responde ao tweet
                client.create_tweet(
                    text=f"@{mention.author_id} Hello World!",
                    in_reply_to_tweet_id=mention.id,
                )

                print("Resposta enviada com sucesso!")
            except Exception as e:
                print(f"Erro ao responder: {e}")
    else:
        print("Nenhuma menção encontrada.")

# Executa a função
if __name__ == "__main__":
    print("Bot iniciado. Respondendo às menções...")
    reply_to_mentions()
    print("Execução concluída.")


