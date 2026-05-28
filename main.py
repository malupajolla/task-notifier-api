from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, notifier

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

BOT_TOKEN = "8758364347:AAEl7mlSpK4Xr6xpmAQD3N8jCUV_kHlVgVU"

@app.post("/tasks/")
async def criar_tarefa(titulo: str, destinatario: str, db: Session = Depends(database.get_db)):
    nova_tarefa = models.Task(titulo=titulo, destinatario=destinatario)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    
    mensagem = f"✅ Nova tarefa criada: {titulo}"
    try:
        await notifier.enviar_notificacao(mensagem, destinatario, BOT_TOKEN)
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")
        
    return nova_tarefa