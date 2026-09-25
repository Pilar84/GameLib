import os
import logging
import requests

logger = logging.getLogger(__name__)

MAILEROO_URL = "https://smtp.maileroo.com/api/v2/emails"

#esta prueba la realicé para que devolviera un error 503 (timeout/red)
#MAILEROO_URL = "https://10.255.255.1"

def send_welcome_email(to_email):
    logger.info(
        "send_welcome_email: intento de envío",
        extra={"action": "register_welcome", "to": to_email, "result": "attempt"}
    )

    headers = {
        "Authorization": f"Bearer {os.getenv('MAILEROO_TOKEN')}",
        "Content-Type": "application/json",
    }

    payload = {
        "from": {"address": os.getenv("MAILEROO_FROM_ADDRESS")},
        "to": [{"address": to_email}],
        "subject": "Bienvenida a Steamlike",
        "plain": "¡Gracias por registrarte!"
    }

    try:
        r = requests.post(MAILEROO_URL, headers=headers, json=payload, timeout=5)
    except requests.RequestException as e:
        logger.error(
            "send_welcome_email: fallo por timeout/red",
            extra={
                "action": "register_welcome",
                "to": to_email,
                "result": "external_service_unavailable",
                "error": str(e)
            }
        )
        return False

    if r.status_code >= 400:
        logger.error(
            "send_welcome_email: fallo por respuesta del proveedor",
            extra={
                "action": "register_welcome",
                "to": to_email,
                "result": "external_service_error",
                "maileroo_status": r.status_code
            }
        )
        return False

    logger.info(
        "send_welcome_email: envío OK",
        extra={"action": "register_welcome", "to": to_email, "result": "ok"}
    )

    return True
