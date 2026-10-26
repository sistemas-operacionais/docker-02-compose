import socket
import time

HOST = 'produtor'
PORT = 5000

def enviar_mensagem():
    print("Consumidor iniciando, tentando conectar ao PRODUTOR...", flush=True)
    
    # Loop de tentativas para contornar o atraso de inicialização no Codespaces
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3) # Timeout de 3 segundos por tentativa
                print(f"Tentando conectar em {HOST}:{PORT}...", flush=True)
                s.connect((HOST, PORT))
                
                mensagem = "Olá do Produtor via Socket!"
                s.sendall(mensagem.encode('utf-8'))
                
                data = s.recv(1024)
                print(f"Resposta do consumidor: {data.decode('utf-8')}", flush=True)
                break # Conectou e enviou com sucesso, sai do loop
                
        except (socket.error, socket.timeout) as e:
            print(f"Consumidor ainda não está pronto ({e}). Tentando novamente em 2 segundos...", flush=True)
            time.sleep(2)

if __name__ == "__main__":
    enviar_mensagem()