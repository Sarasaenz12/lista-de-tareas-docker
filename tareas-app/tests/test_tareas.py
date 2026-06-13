import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Base de datos SQLite en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_root():
    """Prueba que el endpoint raíz responde correctamente."""
    response = client.get("/")
    assert response.status_code == 200
    assert "mensaje" in response.json()


def test_crear_tarea():
    """Prueba que se puede crear una tarea correctamente."""
    payload = {"titulo": "Aprender Docker", "descripcion": "Completar el taller"}
    response = client.post("/tareas", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Aprender Docker"
    assert data["completada"] is False
    assert "id" in data


def test_listar_tareas():
    """Prueba que el listado de tareas devuelve una lista."""
    response = client.get("/tareas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_eliminar_tarea():
    """Prueba que se puede eliminar una tarea existente."""
    # Crear primero
    nueva = client.post("/tareas", json={"titulo": "Tarea a eliminar"})
    tarea_id = nueva.json()["id"]

    # Eliminar
    response = client.delete(f"/tareas/{tarea_id}")
    assert response.status_code == 204

    # Verificar que ya no existe listándola
    tareas = client.get("/tareas").json()
    ids = [t["id"] for t in tareas]
    assert tarea_id not in ids


def test_eliminar_tarea_inexistente():
    """Prueba que eliminar una tarea inexistente devuelve 404."""
    response = client.delete("/tareas/99999")
    assert response.status_code == 404

def test_actualizar_tarea():
    """Prueba que se puede marcar una tarea como completada."""
    nueva = client.post("/tareas", json={"titulo": "Tarea a actualizar"})
    tarea_id = nueva.json()["id"]

    response = client.patch(f"/tareas/{tarea_id}", json={"completada": True})
    assert response.status_code == 200
    assert response.json()["completada"] is True