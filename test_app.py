import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# Prueba si /hospitales devuelve una lista
def test_get_hospitales(client):
    response = client.get("/hospitales")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)  # Debe ser una lista
    if data:  # Si hay hospitales registrados
        assert "Nombre" in data[0]  # El primer elemento debe tener "Nombre"

# Prueba si /hospital_cercano devuelve un hospital
def test_get_hospital_cercano(client):
    response = client.get("/hospital_cercano?lat=-12.0450&lon=-77.0350")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Nombre" in data  # Debe devolver un hospital con "Nombre"