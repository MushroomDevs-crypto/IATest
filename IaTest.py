import tweepy
import os
from time import sleep
import openai


from dotenv import load_dotenv


openai.api_key = os.getenv("OPENAI_API_KEY")
# Carrega variáveis de ambiente
load_dotenv()

# Credenciais da API do X (Twitter)
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Credenciais da API do ChatGPT (OpenAI)
openai.api_key = os.getenv("OPENAI_API_KEY")


client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    wait_on_rate_limit=True,
)

# Teste de billing DOIS
# Função para obter o ID do usuário autenticado
def get_user_id():
    try:
        user = client.get_user(username="Mushroomdevs")  # Substitua pelo nome de usuário do bot
        return user.data.id
    except Exception as e:
        print(f"Erro ao obter ID do usuário: {e}")
        return None

# Gera uma resposta usando o ChatGPT
def generate_chatgpt_response(tweet_text):
    try:
        # Template para a resposta
        system_prompt = """
        Você é um bot inteligente que responde com sabedoria e clareza. Use um tom profissional, mas amigável.
        
        Formato de resposta:
        - Comece com uma introdução breve.
        - Dê uma resposta objetiva e clara.
        - Conclua com uma frase de fechamento amigável.

        Certifique-se de que sua resposta seja relevante ao texto fornecido.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Modelo a ser usado
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": tweet_text},
            ],
        )
        # Extrai o conteúdo da resposta gerada
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao gerar resposta com ChatGPT: {e}")
        return "Desculpe, algo deu errado ao gerar minha resposta."


# Função para responder a menções com base no tweet original
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
            tweet_fields=["id", "author_id", "referenced_tweets"],
        )
        
        if mentions.data:
            print(f"Encontradas {len(mentions.data)} menções.")
            for mention in mentions.data:
                referenced_tweet_id = None

                # Verifica se há um tweet referenciado (o tweet original)
                if mention.referenced_tweets:
                    for ref in mention.referenced_tweets:
                        if ref["type"] == "replied_to":
                            referenced_tweet_id = ref["id"]
                            break
                
                if not referenced_tweet_id:
                    print(f"Não foi possível encontrar o tweet original para a menção {mention.id}.")
                    continue
                
                # Busca o tweet original
                original_tweet = client.get_tweet(id=referenced_tweet_id, tweet_fields=["text"]).data
                if not original_tweet:
                    print(f"Não foi possível obter o tweet original {referenced_tweet_id}.")
                    continue
                
                # Gera a resposta com base no tweet original
                print(f"Gerando resposta para o tweet {original_tweet.id}...")
                response_text = generate_chatgpt_response(original_tweet.text)

                # Responde à menção
                try:
                    print(f"Respondendo ao tweet {mention.id}...")
                    client.create_tweet(
                        text=response_text,
                        in_reply_to_tweet_id=mention.id,
                    )
                    print(f"Resposta enviada para o tweet {mention.id}.")
                except Exception as e:
                    print(f"Erro ao responder ao tweet {mention.id}: {e}")
                
                # Atualiza o ID da última menção processada
                last_mention_id = mention.id
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




