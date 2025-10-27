# lambdas/criarEntrega/handler.py
import os
import sys
import json

# Garante que podemos importar pacote src quando executado localmente
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from src.services.entrega_service import criar_entrega
from src.utils.resposta import created, bad_request

def handler(event, context=None):
    """
    event expected:
    {
        "cliente": "Nome",
        "origem": "Rua A, 100",
        "destino": "Rua B, 200",
        "meta": {...}  # opcional
    }
    """
    try:
        body = event if isinstance(event, dict) else json.loads(event)
        cliente = body.get("cliente")
        origem = body.get("origem")
        destino = body.get("destino")
        meta = body.get("meta", {})

        if not (cliente and origem and destino):
            return bad_request("cliente, origem e destino são obrigatórios")

        entrega = criar_entrega(cliente, origem, destino, meta)
        # Em ambiente real, aqui publicaríamos na fila de atualizações
        return created(entrega)
    except Exception as e:
        return bad_request(str(e))


# Permite teste rápido:
if __name__ == "__main__":
    ev = {"cliente": "Raphael", "origem": "Rua A", "destino": "Rua B"}
    print(handler(ev))
