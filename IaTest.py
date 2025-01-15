import tweepy

# Substitua pelos seus dados de autenticação
consumer_key = "TWITTER_API_KEY"
consumer_secret = "TWITTER_API_SECRET"
access_token = "TWITTER_ACCESS_TOKEN"
access_token_secret = "TWITTER_ACCESS_TOKEN_SECRET"

# Autenticação
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Cria a API
api = tweepy.API(auth)

# Função para responder a menções
def reply_to_mentions():
    # Obtém os últimos 20 tweets onde o bot foi mencionado
    mentions = api.mentions_timeline(count=20)

    for mention in mentions:
        # Verifica se o tweet ainda não foi respondido
        if not mention.in_reply_to_status_id:
            # Responde ao tweet mencionado
            api.update_status(
                status="Hello World",
                in_reply_to_status_id=mention.id,
                auto_populate_reply_metadata=True  # Adiciona automaticamente os nomes de usuário mencionados
            )
            print(f"Respondido ao tweet de {mention.user.screen_name}")

# Executa a função para responder às menções
reply_to_mentions()

