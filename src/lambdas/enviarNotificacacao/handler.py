# lambdas/enviarNotificacao/handler.py
import os
import sys
import json
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from src.services.entrega_service import get_entrega_by_id
from src.utils.resposta import ok, not_found, bad_request

def handler(event, context=None):
    """
    Simula enviar notificação ao cliente.
    event expected:
    {
      "id": "ent-xxxx",
      "mensagem": "Sua entrega foi entregue!"
    }
    """
    try:
        body = event if isinstance(event, dict) else json.loads(event)
        entrega_id = body.get("id")
        mensagem = body.get("mensagem", "")
        if not entrega_id:
            return bad_request("id obrigatório")

        entrega = get_entrega_by_id(entrega_id)
        if not entrega:
            return not_found("Entrega não encontrada")

        # Simulação: "enviar" a notificação (aqui apenas logamos)
        # Em produção, integrar com SNS, FCM, SMTP, etc.
        time_str = time.strftime("%Y-%m-%d %H:%M:%S")
        log = {
            "to": entrega["cliente"],
            "id": entrega_id,
            "mensagem": mensagem or f"Status: {entrega['status']}",
            "timestamp": time_str
        }
        print("[NOTIF] ", json.dumps(log, ensure_ascii=False))
        return ok({"notificacao": log})
    except Exception as e:
        return bad_request(str(e))

# teste rápido
if __name__ == "__main__":
    ev = {"id": "ent-xxxx", "mensagem": "Sua entrega saiu para entrega"}
    print(handler(ev))
