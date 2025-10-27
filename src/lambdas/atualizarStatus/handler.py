# lambdas/atualizarStatus/handler.py
import os
import sys
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from src.services.entrega_service import atualizar_status, get_entrega_by_id
from src.utils.resposta import ok, not_found, bad_request

def handler(event, context=None):
    """
    event expected:
    {
        "id": "ent-xxxx",
        "status": "em rota"  # ou "entregue", etc
    }
    """
    try:
        body = event if isinstance(event, dict) else json.loads(event)
        entrega_id = body.get("id")
        novo_status = body.get("status")
        if not (entrega_id and novo_status):
            return bad_request("id e status são obrigatórios")

        updated = atualizar_status(entrega_id, novo_status)
        if not updated:
            return not_found("Entrega não encontrada")
        # Em ambiente real, aqui publicaríamos na filaNotificações
        return ok(updated)
    except Exception as e:
        return bad_request(str(e))

# teste rápido
if __name__ == "__main__":
    ev = {"id": "ent-00000000", "status": "em rota"}
    print(handler(ev))
