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


@app.get("/tasks/")
def listar_tarefas(db: Session = Depends(database.get_db)):
    return db.query(models.Task).all()

@app.get("/tasks/{task_id}")
def buscar_tarefa(task_id: int, db: Session = Depends(database.get_db)):
    tarefa = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@app.put("/tasks/{task_id}")
async def atualizar_tarefa(task_id: int, concluida: bool, db: Session = Depends(database.get_db)):
    tarefa = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa.concluida = concluida
    db.commit()
    db.refresh(tarefa)

    mensagem = f"📝 Tarefa atualizada: {tarefa.titulo} — {'concluída ✅' if concluida else 'reaberta 🔄'}"
    try:
        await notifier.enviar_notificacao(mensagem, tarefa.destinatario, BOT_TOKEN)
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")

    return tarefa

@app.delete("/tasks/{task_id}")
async def deletar_tarefa(task_id: int, db: Session = Depends(database.get_db)):
    tarefa = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()

    mensagem = f"🗑️ Tarefa removida: {tarefa.titulo}"
    try:
        await notifier.enviar_notificacao(mensagem, tarefa.destinatario, BOT_TOKEN)
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")

    return {"mensagem": "Tarefa deletada com sucesso"}