# src/services/entrega_service.py
import json
import os
import uuid
from typing import Optional, Dict, List

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_PATH = os.path.join(ROOT, 'src', 'database', 'entregas.json')

def _read_db() -> List[Dict]:
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def _write_db(data: List[Dict]):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def criar_entrega(cliente: str, origem: str, destino: str, meta: Optional[Dict]=None) -> Dict:
    """Cria uma nova entrega e salva no 'NoSQL' (JSON)."""
    entregas = _read_db()
    novo = {
        "id": f"ent-{uuid.uuid4().hex[:8]}",
        "cliente": cliente,
        "origem": origem,
        "destino": destino,
        "status": "pendente",
        "meta": meta or {}
    }
    entregas.append(novo)
    _write_db(entregas)
    return novo

def get_entrega_by_id(entrega_id: str) -> Optional[Dict]:
    entregas = _read_db()
    for e in entregas:
        if e["id"] == entrega_id:
            return e
    return None

def atualizar_status(entrega_id: str, novo_status: str) -> Optional[Dict]:
    entregas = _read_db()
    found = None
    for e in entregas:
        if e["id"] == entrega_id:
            e["status"] = novo_status
            found = e
            break
    if found:
        _write_db(entregas)
    return found

def listar_entregas() -> List[Dict]:
    return _read_db()

# função útil para testes limpar DB local (não para produção)
def _reset_db():
    _write_db([])
