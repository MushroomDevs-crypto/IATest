import tweepy
import os
from time import sleep

# Carregar variáveis de ambiente (ou defina manualmente suas chaves aqui)
from dotenv import load_dotenv
load_dotenv()

# Configurações do Twitter API
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Autenticação no Twitter com OAuth 1.0a
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def respond_to_mentions():
    """Responde automaticamente a menções"""
    try:
        # Obter menções do usuário autenticado
        mentions = api.mentions_timeline(count=10, tweet_mode="extended")
        
        for mention in mentions:
            # Verifica se o bot já respondeu ao tweet
            if mention.favorited:
                continue
            
            print(f"Respondendo à menção: {mention.user.screen_name} - {mention.full_text}")
            
            # Cria a resposta ao tweet
            response_text = f"@{mention.user.screen_name} Hello World!"
            api.update_status(status=response_text, in_reply_to_status_id=mention.id)
            
            # Marca o tweet como 'favoritado' para evitar responder novamente
            api.create_favorite(mention.id)
            print(f"Respondido a {mention.user.screen_name}")
            
            # Pausa entre as respostas para evitar limites de taxa
            sleep(5)
    
    except tweepy.TweepError as e:
        print(f"Erro ao responder menções: {e}")

if __name__ == "__main__":
    print("Bot iniciado. Verificando menções...")
    while True:
        respond_to_mentions()
        print("Aguardando antes de verificar novamente...")
        sleep(60)  # Espera 1 minuto antes de verificar novamente

