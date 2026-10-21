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
$ docker ps -a

# 3. criar `docker-compose.yml`
$ touch docker-compose.yml

# 4. criar 2 conteineres usando o docker compose
$ docker compose up
$ docker ps -a

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

## Referências

- [docker docs](https://docs.docker.com/)
  - [docker compose](https://docs.docker.com/compose/)
- [Docker para desenvolvedores](https://github.com/gomex/docker-para-desenvolvedores/)
  - [Gerenciando múltiplos contêineres docker com Docker Compose](https://github.com/gomex/docker-para-desenvolvedores/blob/master/manuscript/compose.md)
- github
  - codespaces dev container [en](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers) [pt-br](https://docs.github.com/pt/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers)

---