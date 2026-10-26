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

# 5. conectar no serviço consumidor e testar manualmente
$ docker compose ps -a
CONTAINER ID   IMAGE                          COMMAND                  CREATED          STATUS                      PORTS                                         NAMES
8835762c59d1   minha-imagem-python            "python3"                20 minutes ago   Exited (0) 20 minutes ago                                                 conteiner-python
174fa4409e66   docker-02-compose-consumidor   "python consumidor.py"   6 hours ago      Up 12 seconds                                                             docker-02-compose-consumidor-1
4b257d49d105   docker-02-compose-produtor     "python produtor.py"     6 hours ago      Up 13 seconds               0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   docker-02-compose-produtor-1
82adcc86d9c9   meu-app-python                 "/bin/bash"              2 days ago       Exited (130) 2 days ago                                                   teste

$ docker exec -it 174fa4409e66 /bin/bash
root@174fa4409e66: 

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

---

## Referências

- [docker docs](https://docs.docker.com/)
  - [docker compose](https://docs.docker.com/compose/)
- [Docker para desenvolvedores](https://github.com/gomex/docker-para-desenvolvedores/)
  - [Gerenciando múltiplos contêineres docker com Docker Compose](https://github.com/gomex/docker-para-desenvolvedores/blob/master/manuscript/compose.md)
- github
  - codespaces dev container [en](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers) [pt-br](https://docs.github.com/pt/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers)

---