from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TareaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None

class TareaCreate(TareaBase):
    pass

class TareaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    completada: Optional[bool] = None

class TareaResponse(TareaBase):
    id: int
    completada: bool
    creada_en: datetime

    model_config = {"from_attributes": True}