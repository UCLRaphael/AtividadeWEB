# tests/test_entrega.py
import os
import sys
import json
import pytest

# Ajusta path para importar src
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from src.services.entrega_service import criar_entrega, atualizar_status, get_entrega_by_id, _reset_db

@pytest.fixture(autouse=True)
def run_around_tests():
    # antes de cada teste, limpa o DB mock
    _reset_db()
    yield
    _reset_db()

def test_criar_entrega():
    e = criar_entrega("Teste", "Origem", "Destino")
    assert e["cliente"] == "Teste"
    assert e["status"] == "pendente"
    assert "id" in e

def test_atualizar_status():
    e = criar_entrega("Teste", "A", "B")
    ent_id = e["id"]
    updated = atualizar_status(ent_id, "em rota")
    assert updated is not None
    assert updated["status"] == "em rota"
    fetched = get_entrega_by_id(ent_id)
    assert fetched["status"] == "em rota"

def test_atualizar_status_entrega_inexistente():
    updated = atualizar_status("ent-inexistente", "em rota")
    assert updated is None
