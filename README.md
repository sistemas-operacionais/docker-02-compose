# Notas de aula de Docker Compose

## Informações gerais

- **Público alvo**: alunos da disciplina de **Sistemas operacionais** do curso de [TADS](https://diatinf.ifrn.edu.br/cursos/tecnologia-em-analise-e-desenvolvimento-de-sistemas/) na [DIATINF](https://diatinf.ifrn.edu.br/) no [CNAT-IFRN](https://portal.ifrn.edu.br/campus/natalcentral/)
- **Professor**: [L A Minora](https://github.com/leonardo-minora/)
- **Objetivo**:
  1. Apresentar conceito introdutório sobre docker compose

---
### Sessão de introdução
1. criar um `Dockerfile` python e compilar a imagem
2. criar um conteiner com a nova imagem para testar
3. criar `docker-compose.yml`
4. criar 2 conteineres usando o docker compose

```bash
# 1. criar um `Dockerfile` python e compilar a imagem
$ touch Dockerfile
$ docker build -t minha-imagem-python .

# 2. criar um conteiner com a nova imagem para testar
$ docker run -it --name conteiner-python minha-imagem-python
Python 3.15.0 (main, Oct 21 2026, 03:30:42) [GCC 14.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit

$ docker ps -a
CONTAINER ID   IMAGE                 COMMAND     CREATED         STATUS                     PORTS     NAMES
7439d2a3d236   minha-imagem-python   "python3"   9 seconds ago   Exited (0) 5 seconds ago             conteiner-python

$ docker rm 7439d2a3d236

# 3. criar `docker-compose.yml`
$ touch docker-compose.yml

# 4. criar 2 conteineres usando o docker compose
$ docker compose up
$ docker compose ps -a

```
**Dockerfile**
```dockerfile
FROM python:3

WORKDIR /app

```

**docker-compose.yml**
```yml
services:
  consumidor:
    build: .
    depends_on:
      - produtor
  produtor:
    build: .

```

---
### Sessão com os serviços comunicando
1. criar os arquivos python de produtor e consumidor
2. modificar o arquivo `docker-compose.yml` para mapear de pasta do hospereiro para conteineres
3. adicionar comando python para executar produtor e consumidor
4. modificar o arquivo `docker-compose.yml` para mapear porta do hospedeiro para conteiner produtor (servidor)
4. inicializar serviços produtor e consumidor
5. conectar no serviço consumidor e testar manualmente

```bash
# 1. criar os arquivos python de produtor e consumidor
$ touch /src/python/consumidor.py
$ touch /src/python/produtor.py

# 2. modificar o arquivo `docker-compose.yml` para mapear de pasta do hospereiro para conteineres
###     volumes:
###      - ./src/python:/app

# 3. adicionar comando python para executar produtor e consumidor
###    command: python consumidor.py
###    command: python produtor.py

# 4. modificar o arquivo `docker-compose.yml` para mapear porta do hospedeiro para conteiner produtor (servidor)
###    ports:
###      - "5000:5000"

# 4. inicializar serviços produtor e consumidor
$ docker compose up
# Para finalizar pressionar CTRL+D 
# Exemplo de saída abaixo
WARN[0000] Found orphan containers (docker-02-compose-produtor-run-e0cf59ed37ed, docker-02-compose-consumidor-run-e5fb593d0911) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
[+] up 1/1
 ✔ Container docker-02-compose-produtor-1 Running                                                                                                           0.0s
Attaching to consumidor-1, produtor-1
consumidor-1  | Consumidor iniciando, tentando conectar ao PRODUTOR...
consumidor-1  | Tentando conectar em host.docker.internal:5000...
produtor-1    | Conectado por: ('172.18.0.1', 40082)
produtor-1    | Mensagem recebida: Olá do Produtor via Socket!
consumidor-1  | Resposta do consumidor: Mensagem recebida com sucesso!
consumidor-1 exited with code 0
## Após presssionar CTRL+D
Container docker-02-compose-consumidor-1 Stopping 
Container docker-02-compose-consumidor-1 Stopped 
Container docker-02-compose-produtor-1 Stopping 
Container docker-02-compose-produtor-1 Stopped 
produtor-1 exited with code 137

# 5. conectar no serviço consumidor e testar manualmente
$ docker compose ps -a
# Exemplo de saída abaixo
NAME                                            IMAGE                          COMMAND                  SERVICE      CREATED         STATUS     PORTS
docker-02-compose-consumidor-1                  docker-02-compose-consumidor   "python consumidor.py"   consumidor   7 minutes ago   Exited (0) About a minute ago   
docker-02-compose-produtor-1                    docker-02-compose-produtor     "python -u produtor.…"   produtor     7 minutes ago   Exited (137) 29 seconds ago     

```

**docker-compose.yml**
```yml
services:
  consumidor:
    build: .
    command: python consumidor.py
    volumes:
      - ./src/python:/app
    depends_on:
      - produtor
  produtor:
    build: .
    command: python produtor.py
    ports:
      - "5000:5000"
    volumes:
      - ./src/python:/app

```

**/src/python/produtor.py**
```python
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
                conn.settimeout(3)
                print(f"Conectado por: {addr}")
                try:
                    data = conn.recv(1024)
                except socket.timeout:
                    continue
                if not data:
                    continue
                print(f"Mensagem recebida: {data.decode('utf-8', errors='replace')}")
                conn.sendall(b"Mensagem recebida com sucesso!")

if __name__ == "__main__":
    iniciar_servidor()
    
```

**/src/python/consumidor.py**
```python
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

```

**Observações**: 
- o código acima funcionou na aula, contudo logo após a aula apresentou problema de comunicação em algumas tentativas de execução em casa.
- após algum diálogo com o gemini e copilot (esse dentro do vs code), a solução foi colocar um "novo nome de endereço" e usá-lo no código consumidor.
- mudou `docker-compose.yml` e `consumidor.py`, que ficou como os arquivos abaixo.

**docker-compose.yml**
```yml
services:
  consumidor:
    build: .
    command: python consumidor.py
    volumes:
      - ./src/python:/app
    extra_hosts:
      - "host.docker.internal:host-gateway"
    depends_on:
      - produtor
  produtor:
    build: .
    command: python -u produtor.py
    ports:
      - "5000:5000"
    volumes:
      - ./src/python:/app
      
``` 

**/src/python/consumidor.py**
```python
import socket
import time

HOST = 'host.docker.internal'
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

```

---

## Referências

- [docker docs](https://docs.docker.com/)
  - [docker compose](https://docs.docker.com/compose/)
- [Docker para desenvolvedores](https://github.com/gomex/docker-para-desenvolvedores/)
  - [Gerenciando múltiplos contêineres docker com Docker Compose](https://github.com/gomex/docker-para-desenvolvedores/blob/master/manuscript/compose.md)
- github
  - codespaces dev container [en](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers) [pt-br](https://docs.github.com/pt/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers)

---