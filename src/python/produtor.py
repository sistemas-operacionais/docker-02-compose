import socket

HOST = '0.0.0.0'  # Escuta em todas as interfaces de rede do container
PORT = 5000       # Porta interna do serviço

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"PRODUTOR aguardando conexões na porta {PORT}...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conectado por: {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Mensagem recebida: {data.decode('utf-8')}")
                conn.sendall(b"Mensagem recebida com sucesso!")

if __name__ == "__main__":
    iniciar_servidor()