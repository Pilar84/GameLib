import requests
from django.core.cache import cache
import logging
logger = logging.getLogger(__name__)

CHEAPSHARK_URL = "https://www.cheapshark.com/api/1.0/games"
CHEAPSHARK_HEADERS = {
    "User-Agent": "Steamlike/1.0 (educational project; contact: student@example.com)",
    "Accept": "application/json",
}


class CatalogService:

    @staticmethod
    def search(query: str):
        query_clean = query.strip().lower()
        cache_key = f"catalog_search:{query_clean}"

        # 1. Intentar obtener de Redis
        logger.info(f"[catalog_search] Consultando Redis | key={cache_key}")
        cached = cache.get(cache_key)

        if cached is not None:
            logger.info(f"[catalog_search] Usando datos cacheados | key={cache_key}")
            return cached, None

        # 2. Llamar a CheapShark
        logger.info(f"[catalog_search] Consultando proveedor externo CheapShark | query={query_clean}")
        try:
            response = requests.get(
                CHEAPSHARK_URL,
                params={"title": query},
                headers=CHEAPSHARK_HEADERS,
                timeout=5
            )
        except requests.RequestException:
            logger.warning(f"[catalog_search] Fallo de red/timeout con CheapShark | query={query_clean}")

            if cached is not None:
                logger.info(f"[catalog_search] Usando Redis por fallo del proveedor | key={cache_key}")
                return cached, None

            return None, "external_unavailable"

        # 3. CheapShark respondió pero con error
        if response.status_code != 200:
            logger.error(f"[catalog_search] Error del proveedor externo | status={response.status_code}")

            if cached is not None:
                logger.info(f"[catalog_search] Usando Redis por fallo del proveedor | key={cache_key}")
                return cached, None

            return None, "external_error"

        # 4. Procesar datos correctos
        cheapshark_data = response.json()

        results = []
        for game in cheapshark_data:
            results.append({
                "external_game_id": game.get("gameID"),
                "title": game.get("external"),
                "thumb": game.get("thumb")
            })

        # 5. Guardar en Redis
        cache.set(cache_key, results, timeout=60 * 3)
        logger.info(f"[catalog_search] Datos guardados en Redis | key={cache_key}")

        return results, None

    @staticmethod
    def resolve(external_ids: list[str]):
        logger.info(f"[catalog_resolve] Resolviendo IDs | ids={external_ids}")

        try:
            response = requests.get(
                CHEAPSHARK_URL,
                params={"ids": ",".join(external_ids)},
                headers=CHEAPSHARK_HEADERS,
                timeout=5
            )
        except requests.RequestException:
            logger.warning(f"[catalog_resolve] Fallo de red/timeout con CheapShark | ids={external_ids}")
            return None, "external_unavailable"

        if response.status_code != 200:
            logger.error(f"[catalog_resolve] Error del proveedor externo | status={response.status_code}")
            return None, "external_error"

        cheapshark_data = response.json()

        results = []
        for game_id, game_info in cheapshark_data.items():
            info = game_info.get("info", {})
            results.append({
                "external_game_id": game_id,
                "title": info.get("title"),
                "thumb": info.get("thumb")
            })

        logger.info(f"[catalog_resolve] Datos obtenidos correctamente | count={len(results)}")

        return results, None