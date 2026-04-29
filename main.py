from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

app = FastAPI(title="Gerenciador de Tarefas API")

@app.post("/tarefas", response_model=schemas.TarefaResponse, status_code=status.HTTP_201_CREATED)
def criar_tarefa(tarefa: schemas.TarefaCreate, db: Session = Depends(get_db)):
    nova_tarefa = models.Tarefa(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao
    )
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

@app.get("/tarefas", response_model=List[schemas.TarefaResponse])
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(models.Tarefa).all()

@app.get("/tarefas/{tarefa_id}", response_model=schemas.TarefaResponse)
def obter_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@app.put("/tarefas/{tarefa_id}", response_model=schemas.TarefaResponse)
def atualizar_tarefa(tarefa_id: int, tarefa_update: schemas.TarefaCreate, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    tarefa.titulo = tarefa_update.titulo
    tarefa.descricao = tarefa_update.descricao
    
    db.commit()
    db.refresh(tarefa)
    return tarefa

@app.patch("/tarefas/{tarefa_id}/concluir", response_model=schemas.TarefaResponse)
def concluir_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    tarefa.concluida = True
    db.commit()
    db.refresh(tarefa)
    return tarefa

@app.delete("/tarefas/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    db.delete(tarefa)
    db.commit()
    return None
