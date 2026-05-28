import httpx

async def enviar_notificacao(mensagem: str, chat_id: str, bot_token: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={
            "chat_id": chat_id,
            "text": mensagem
        })