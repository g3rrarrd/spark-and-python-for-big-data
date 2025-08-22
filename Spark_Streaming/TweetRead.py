import tweepy
import socket
import time


bearer_token = 'AAAAAAAAAAAAAAAAAAAAALXj3gEAAAAAqqkaiGg1nvygFoVnKUw9I1%2BWkt4%3DkDHvNoKZYfmbDamW7JK0Y5JPYHq64CeK2ZTKIgY42Hvjptj91G'

client = tweepy.Client(bearer_token=bearer_token)

def sendData(c_socket):
    query = "guitar -is:retweet lang:en"
    last_seen_id = None

    while True:
        try:
            if last_seen_id:
                response = client.search_recent_tweets(
                    query=query,
                    since_id=last_seen_id,
                    max_results=10,
                    tweet_fields=["created_at"]
                )
            else:
                response = client.search_recent_tweets(
                    query=query,
                    max_results=10,
                    tweet_fields=["created_at"]
                )

            if response.data:
                print(f"Se recibieron {len(response.data)} tweets")
                for tweet in reversed(response.data):  # más antiguos primero
                    text = f"{tweet.id} | {tweet.created_at} | {tweet.text}\n"
                    print(">>", text.strip())
                    c_socket.send(text.encode("utf-8"))
                # 👇 usar el último (más viejo) para que no se vacíe el stream
                last_seen_id = response.data[-1].id
            else:
                print("⚠️ No se encontraron tweets nuevos en esta iteración.")

            time.sleep(10)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(15)

if __name__ == "__main__":
    s = socket.socket()
    host = "127.0.0.1"
    port = 5555
    s.bind((host, port))

    print(f"Servidor escuchando en {host}:{port} ...")

    s.listen(5)
    c, addr = s.accept()
    print("Cliente conectado desde:", addr)

    sendData(c)