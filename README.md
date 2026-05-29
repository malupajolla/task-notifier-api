# Task Notifier API

API REST para gerenciamento de tarefas com notificações em tempo real via Telegram, desenvolvida com Python e FastAPI.

## Sobre o projeto

Sistema que permite criar, listar, atualizar e deletar tarefas, enviando automaticamente notificações no Telegram a cada ação realizada. Conta com interface web interativa feita com Streamlit.

## Funcionalidades

- Criar tarefas com notificação automática no Telegram
- Listar todas as tarefas
- Marcar tarefas como concluídas ou reabrir
- Deletar tarefas com notificação
- Interface web interativa com Streamlit

## Tecnologias

- Python 3.x
- FastAPI
- SQLAlchemy + SQLite
- Streamlit
- Telegram Bot API

## Como rodar

1. Clone o repositório:
   git clone https://github.com/malupajolla/task-notifier-api

2. Instale as dependências:
   python -m pip install fastapi uvicorn sqlalchemy httpx streamlit requests

3. Configure seu bot no arquivo main.py:
   BOT_TOKEN = "seu_token_aqui"

4. Rode a API:
   python -m uvicorn main:app --reload

5. Em outro terminal, rode a interface:
   python -m streamlit run interface.py

## Como obter o Chat ID do Telegram

1. Pesquise @BotFather no Telegram e crie um bot
2. Pesquise @userinfobot para pegar seu Chat ID
3. Inicie uma conversa com seu bot antes de testar

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /tasks/ | Lista todas as tarefas |
| POST | /tasks/ | Cria uma tarefa |
| PUT | /tasks/{id} | Atualiza uma tarefa |
| DELETE | /tasks/{id} | Deleta uma tarefa |

## Autora

Maria Luiza Pajolla