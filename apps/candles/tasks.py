# app/candles/tasks.py
from celery import shared_task
from .models import Candle
from apps.markets.models import PairTracking
import requests  
from django.db.models import Max
from decimal import Decimal
import logging
from celery import group
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# ---------------------------------------
# Task principal: dispara subtasks por par
# ---------------------------------------
@shared_task
def fetch_all_candles_task(max_candles_per_pair=5000):
    """
    Busca todos los pares activos y lanza subtasks para cada uno.
    """
    pairs = PairTracking.objects.filter(
        active=True,
        timeframe__active=True,
        pair__active=True
    )

    logger.info(f"🌐 Iniciando fetch para {pairs.count()} pares activos")

    # Crear grupo de subtasks para paralelizar
    tasks = group(fetch_candles_for_pair.s(pair.id, max_candles_per_pair) for pair in pairs)
    result = tasks.apply_async()

    return {"success": True, "total_pairs": pairs.count(), "task_group_id": result.id}


# ---------------------------------------
# Subtask por par
# ---------------------------------------
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def fetch_candles_for_pair(self, pair_id, max_candles=5000):
    
    """
    Fetch y procesa candles para un par específico, luego limpia por cantidad.
    """
    result_data = {
        "pair_id": pair_id,
        "nuevos_candles": 0,
        "deleted_old": 0,
        "success": False,
        "errors": [],
    }

    try:
        pair = PairTracking.objects.get(pk=pair_id)
    except PairTracking.DoesNotExist:
        msg = f"PairTracking no existe: {pair_id}"
        logger.warning(msg)
        result_data["errors"].append(msg)
        return result_data

    # Obtener último timestamp
    last_timestamp = (
        Candle.objects.filter(pair_tracking=pair)
        .aggregate(Max("timestamp"))["timestamp__max"]
    )

    symbol = pair.pair.symbol.replace("/", "").upper()
    url = f"https://fapi.bitunix.com/api/v1/futures/market/kline"
    params = {
        "symbol": symbol,
        "interval": pair.timeframe.name,
        "limit": 1000,
    }
   

    try:
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json().get("data", [])
        print(url)
       

    except requests.exceptions.RequestException as e:
        msg = f"Error en request para {pair}: {e}"
        logger.error(msg)
        result_data["errors"].append(msg)
        raise self.retry(exc=e)

    # Procesar candles
    nuevos_candles = 0
    candles_to_create = []

    for candle_data in data:
        try:
            # timestamp en datetime
            candle_time = datetime.fromtimestamp(int(candle_data["time"]) / 1000, tz=timezone.utc)
            # Saltar candles antiguos
            if last_timestamp and candle_time <= last_timestamp:
                continue

            volume = Decimal(candle_data.get("quoteVol") or 0)
           
            candles_to_create.append(
                Candle(
                    pair_tracking=pair,
                    timestamp=candle_time,
                    timestamp_unix=int(candle_data["time"]),
                    open=Decimal(candle_data["open"]),
                    high=Decimal(candle_data["high"]),
                    low=Decimal(candle_data["low"]),
                    close=Decimal(candle_data["close"]),
                    volume=volume,
                )
            )

        except (KeyError, ValueError, TypeError) as e:
            msg = f"Error procesando candle {candle_data}: {e}"
            logger.warning(msg)
            result_data["errors"].append(msg)
            continue

    if candles_to_create:
        Candle.objects.bulk_create(candles_to_create, ignore_conflicts=True)
        nuevos_candles = len(candles_to_create)
        logger.info(f"✅ Creados {nuevos_candles} nuevos candles para {pair}")

    result_data["nuevos_candles"] = nuevos_candles

    # Limpiar velas antiguas por cantidad
    total_candles = Candle.objects.filter(pair_tracking=pair).count()
    if total_candles > max_candles:
        to_delete = total_candles - max_candles
        old_candles_qs = (
            Candle.objects.filter(pair_tracking=pair)
            .order_by('timestamp')[:to_delete]
        )
        deleted_count, _ = old_candles_qs.delete()
        result_data["deleted_old"] = deleted_count
        if deleted_count:
            logger.info(f"🧹 Eliminadas {deleted_count} velas antiguas para {pair}")

    result_data["success"] = True
    return result_data