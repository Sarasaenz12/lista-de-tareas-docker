from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from contextlib import asynccontextmanager

from app.database import get_db, engine
from app import models, schemas

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Lista de Tareas API", version="1.0.0", lifespan=lifespan)


@app.get("/", tags=["Health"])
def root():
    return {"mensaje": "API de Lista de Tareas funcionando correctamente"}

@app.post("/tareas", response_model=schemas.TareaResponse, status_code=201, tags=["Tareas"])
def crear_tarea(tarea: schemas.TareaCreate, db: Session = Depends(get_db)):
    nueva = models.Tarea(**tarea.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.get("/tareas", response_model=List[schemas.TareaResponse], tags=["Tareas"])
def listar_tareas(db: Session = Depends(get_db)):
    return db.query(models.Tarea).all()

@app.delete("/tareas/{tarea_id}", status_code=204, tags=["Tareas"])
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea)
    db.commit()

@app.patch("/tareas/{tarea_id}", response_model=schemas.TareaResponse, tags=["Tareas"])
def actualizar_tarea(tarea_id: int, datos: schemas.TareaUpdate, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(tarea, campo, valor)
    db.commit()
    db.refresh(tarea)
    return tarea