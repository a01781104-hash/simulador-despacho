"""
Cliente para los Web Services de CENACE.

Implementa:
- Batching automático en ventanas de ≤7 días (restricción de CENACE).
- Caché en disco (JSON) para no repetir llamadas.
- Reintentos con backoff exponencial.
- Validación temporal: huecos, duplicados, negativos.

Servicio principal: SWCAEZC (Cantidades Asignadas de Energía por Zona de Carga)
URL base: https://ws01.cenace.gob.mx:8082/SWCAEZC/SIM/

Referencia: Manual Técnico SW-CAEZC v1 (CENACE, marzo 2018)
"""

import os
import json
import time
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
import requests

# ─── Configuración ───
logger = logging.getLogger(__name__)

BASE_URL = "https://ws01.cenace.gob.mx:8082"
MAX_DAYS_PER_REQUEST = 7  # Restricción de CENACE
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # segundos base (se multiplica por intento)
REQUEST_TIMEOUT = 30  # segundos
DELAY_BETWEEN_REQUESTS = 1.5  # segundos entre llamadas (rate limiting)

SISTEMAS_VALIDOS = ["SIN", "BCA", "BCS"]
PROCESOS_VALIDOS = ["MDA", "MTR"]

# Directorio de caché (relativo al proyecto)
CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"


def _ensure_cache_dir():
    """Crea el directorio de caché si no existe."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_key(servicio: str, sistema: str, proceso: str,
               fecha_ini: str, fecha_fin: str,
               zonas: Optional[str] = None) -> str:
    """
    Genera una clave única para el caché basada en los parámetros de consulta.
    Devuelve un nombre de archivo seguro.
    """
    raw = f"{servicio}_{sistema}_{proceso}_{zonas or 'ALL'}_{fecha_ini}_{fecha_fin}"
    hashed = hashlib.md5(raw.encode()).hexdigest()[:10]
    safe_name = f"{servicio}_{sistema}_{proceso}_{fecha_ini}_{fecha_fin}_{hashed}.json"
    return safe_name


def _load_from_cache(cache_file: str) -> Optional[dict]:
    """Intenta cargar datos del caché en disco."""
    path = CACHE_DIR / cache_file
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"Caché hit: {cache_file}")
            return data
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Caché corrupto ({cache_file}): {e}")
    return None


def _save_to_cache(cache_file: str, data: dict):
    """Guarda datos en caché en disco."""
    _ensure_cache_dir()
    path = CACHE_DIR / cache_file
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        logger.info(f"Caché guardado: {cache_file}")
    except IOError as e:
        logger.warning(f"No se pudo guardar caché ({cache_file}): {e}")


def _fetch_single_batch(url: str, retries: int = MAX_RETRIES) -> dict:
    """
    Hace un GET a la URL con reintentos y backoff exponencial.
    Devuelve el JSON parseado o lanza excepción si falla.
    """
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Request (intento {attempt}): {url}")
            resp = requests.get(url, timeout=REQUEST_TIMEOUT, verify=True)
            resp.raise_for_status()
            data = resp.json()

            # Verificar status de CENACE
            if data.get("status") != "OK":
                raise ValueError(
                    f"CENACE respondió con status: {data.get('status', 'desconocido')}"
                )
            return data

        except requests.exceptions.Timeout:
            last_error = f"Timeout después de {REQUEST_TIMEOUT}s"
            logger.warning(f"Intento {attempt}: {last_error}")
        except requests.exceptions.ConnectionError as e:
            last_error = f"Error de conexión: {e}"
            logger.warning(f"Intento {attempt}: {last_error}")
        except requests.exceptions.HTTPError as e:
            last_error = f"HTTP error: {e}"
            logger.warning(f"Intento {attempt}: {last_error}")
        except (json.JSONDecodeError, ValueError) as e:
            last_error = f"Error de datos: {e}"
            logger.warning(f"Intento {attempt}: {last_error}")

        if attempt < retries:
            wait = RETRY_BACKOFF * attempt
            logger.info(f"Esperando {wait}s antes de reintentar...")
            time.sleep(wait)

    raise ConnectionError(
        f"Falló después de {retries} intentos. Último error: {last_error}"
    )


def _build_url(servicio: str, sistema: str, proceso: str,
               fecha_ini: datetime, fecha_fin: datetime,
               zonas: Optional[str] = None,
               formato: str = "JSON") -> str:
    """
    Construye la URL completa para el web service de CENACE.

    Parámetros de URL (separados por /):
      sistema/proceso/[zonas_carga/]año_ini/mes_ini/dia_ini/año_fin/mes_fin/dia_fin/formato
    """
    parts = [
        BASE_URL,
        servicio,
        "SIM",
        sistema,
        proceso,
    ]

    if zonas:
        parts.append(zonas)

    parts.extend([
        fecha_ini.strftime("%Y"),
        fecha_ini.strftime("%m"),
        fecha_ini.strftime("%d"),
        fecha_fin.strftime("%Y"),
        fecha_fin.strftime("%m"),
        fecha_fin.strftime("%d"),
        formato,
    ])

    return "/".join(parts)


def _date_batches(fecha_ini: datetime, fecha_fin: datetime,
                  max_days: int = MAX_DAYS_PER_REQUEST):
    """
    Divide un rango de fechas en batches de máximo `max_days` días.
    Genera tuplas (batch_inicio, batch_fin).
    """
    current = fecha_ini
    while current <= fecha_fin:
        batch_end = min(current + timedelta(days=max_days - 1), fecha_fin)
        yield (current, batch_end)
        current = batch_end + timedelta(days=1)


def _parse_caezc_resultados(data: dict) -> pd.DataFrame:
    """
    Parsea la respuesta JSON del SWCAEZC a un DataFrame limpio.

    Maneja el hecho de que CENACE devuelve los valores como STRINGS
    (confirmado con datos reales de la API).
    """
    rows = []
    sistema = data.get("sistema", "")
    proceso = data.get("proceso", "")

    for resultado in data.get("Resultados", []):
        zona = resultado.get("zona_carga", "")
        for valor in resultado.get("Valores", []):
            rows.append({
                "sistema": sistema,
                "proceso": proceso,
                "zona_carga": zona,
                "fecha": valor.get("fecha", ""),
                "hora": int(valor.get("hora", 0)),
                "demanda_mdo_nodales": float(valor.get("demanda_mdo_nodales", 0)),
                "demanda_pml_zonales": float(valor.get("demanda_pml_zonales", 0)),
                "total_cargas": float(valor.get("total_cargas", 0)),
            })

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    # Crear timestamp completo: fecha + hora (CENACE usa hora 1-24)
    df["timestamp"] = pd.to_datetime(df["fecha"]) + pd.to_timedelta(
        df["hora"] - 1, unit="h"
    )

    return df


def fetch_demanda(
    sistema: str,
    fecha_ini: str,
    fecha_fin: str,
    proceso: str = "MDA",
    zonas: Optional[str] = None,
    use_cache: bool = True,
    progress_callback=None,
) -> pd.DataFrame:
    """
    Descarga la demanda horaria de CENACE para un sistema eléctrico.

    Parámetros
    ----------
    sistema : str
        Sistema eléctrico: "SIN", "BCA" o "BCS".
    fecha_ini : str
        Fecha inicial en formato "YYYY-MM-DD".
    fecha_fin : str
        Fecha final en formato "YYYY-MM-DD".
    proceso : str
        Tipo de proceso: "MDA" (default) o "MTR".
    zonas : str, opcional
        Zonas de carga separadas por comas (sin espacios).
        Si None, descarga TODAS las zonas del sistema.
    use_cache : bool
        Si True (default), usa caché en disco.
    progress_callback : callable, opcional
        Función que recibe (batch_actual, total_batches) para mostrar progreso.

    Retorna
    -------
    pd.DataFrame
        DataFrame con columnas: sistema, proceso, zona_carga, fecha, hora,
        demanda_mdo_nodales, demanda_pml_zonales, total_cargas, timestamp.

    Raises
    ------
    ValueError
        Si los parámetros son inválidos.
    ConnectionError
        Si CENACE no responde después de todos los reintentos.
    """
    # ── Validaciones ──
    sistema = sistema.upper()
    proceso = proceso.upper()

    if sistema not in SISTEMAS_VALIDOS:
        raise ValueError(
            f"Sistema '{sistema}' no válido. Usar: {SISTEMAS_VALIDOS}"
        )
    if proceso not in PROCESOS_VALIDOS:
        raise ValueError(
            f"Proceso '{proceso}' no válido. Usar: {PROCESOS_VALIDOS}"
        )

    dt_ini = datetime.strptime(fecha_ini, "%Y-%m-%d")
    dt_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

    if dt_ini > dt_fin:
        raise ValueError("fecha_ini debe ser anterior o igual a fecha_fin")

    # ── Dividir en batches ──
    batches = list(_date_batches(dt_ini, dt_fin))
    total_batches = len(batches)
    all_dfs = []

    for i, (b_ini, b_fin) in enumerate(batches):
        b_ini_str = b_ini.strftime("%Y-%m-%d")
        b_fin_str = b_fin.strftime("%Y-%m-%d")

        # Intentar caché primero
        cache_file = _cache_key("SWCAEZC", sistema, proceso, b_ini_str, b_fin_str, zonas)

        if use_cache:
            cached = _load_from_cache(cache_file)
            if cached is not None:
                df_batch = _parse_caezc_resultados(cached)
                if not df_batch.empty:
                    all_dfs.append(df_batch)
                    if progress_callback:
                        progress_callback(i + 1, total_batches)
                    continue

        # No hay caché → llamar a CENACE
        url = _build_url("SWCAEZC", sistema, proceso, b_ini, b_fin, zonas)

        try:
            data = _fetch_single_batch(url)
            # Guardar en caché
            if use_cache:
                _save_to_cache(cache_file, data)
            # Parsear
            df_batch = _parse_caezc_resultados(data)
            if not df_batch.empty:
                all_dfs.append(df_batch)
        except ConnectionError as e:
            # Intentar fallback a caché viejo
            logger.error(f"Batch {b_ini_str} a {b_fin_str} falló: {e}")
            cached = _load_from_cache(cache_file)
            if cached is not None:
                logger.info("Usando caché antiguo como fallback")
                df_batch = _parse_caezc_resultados(cached)
                if not df_batch.empty:
                    all_dfs.append(df_batch)
            else:
                logger.error(f"Sin caché disponible para {b_ini_str}-{b_fin_str}")

        if progress_callback:
            progress_callback(i + 1, total_batches)

        # Rate limiting: esperar entre llamadas
        if i < total_batches - 1:
            time.sleep(DELAY_BETWEEN_REQUESTS)

    if not all_dfs:
        return pd.DataFrame()

    df = pd.concat(all_dfs, ignore_index=True)
    df = df.sort_values(["sistema", "zona_carga", "timestamp"]).reset_index(drop=True)
    return df


def get_demanda_total_sistema(
    sistema: str,
    fecha_ini: str,
    fecha_fin: str,
    proceso: str = "MDA",
    use_cache: bool = True,
    progress_callback=None,
) -> pd.DataFrame:
    """
    Obtiene la demanda TOTAL horaria de un sistema (suma de todas las zonas).

    Retorna DataFrame con columnas: timestamp, fecha, hora, total_cargas_mw
    donde total_cargas_mw es la suma de total_cargas de todas las zonas de carga.
    """
    df = fetch_demanda(
        sistema=sistema,
        fecha_ini=fecha_ini,
        fecha_fin=fecha_fin,
        proceso=proceso,
        use_cache=use_cache,
        progress_callback=progress_callback,
    )

    if df.empty:
        return pd.DataFrame()

    # Sumar demanda de todas las zonas para cada timestamp
    df_total = (
        df.groupby(["timestamp", "fecha", "hora"], as_index=False)
        .agg(total_cargas_mw=("total_cargas", "sum"))
    )

    df_total["sistema"] = sistema
    df_total = df_total.sort_values("timestamp").reset_index(drop=True)
    return df_total


def validate_demand_data(df: pd.DataFrame) -> dict:
    """
    Valida la calidad de los datos de demanda descargados.

    Retorna un diccionario con el reporte de calidad:
    - total_rows: registros totales
    - date_range: (fecha_min, fecha_max)
    - missing_hours: horas faltantes (huecos)
    - duplicate_hours: horas duplicadas
    - negative_values: registros con demanda negativa
    - nan_values: registros con NaN
    - coverage_pct: porcentaje de cobertura horaria
    """
    report = {
        "total_rows": len(df),
        "date_range": None,
        "missing_hours": 0,
        "duplicate_hours": 0,
        "negative_values": 0,
        "nan_values": 0,
        "coverage_pct": 0.0,
    }

    if df.empty:
        return report

    report["date_range"] = (
        df["timestamp"].min().strftime("%Y-%m-%d %H:%M"),
        df["timestamp"].max().strftime("%Y-%m-%d %H:%M"),
    )

    # Horas esperadas
    expected_range = pd.date_range(
        start=df["timestamp"].min(),
        end=df["timestamp"].max(),
        freq="h",
    )
    expected_hours = len(expected_range)

    # Duplicados
    dupes = df.duplicated(subset=["timestamp"], keep=False).sum()
    report["duplicate_hours"] = int(dupes)

    # Huecos
    actual_hours = df["timestamp"].nunique()
    report["missing_hours"] = max(0, expected_hours - actual_hours)

    # Negativos
    if "total_cargas_mw" in df.columns:
        col = "total_cargas_mw"
    elif "total_cargas" in df.columns:
        col = "total_cargas"
    else:
        col = None

    if col:
        report["negative_values"] = int((df[col] < 0).sum())
        report["nan_values"] = int(df[col].isna().sum())

    # Cobertura
    if expected_hours > 0:
        report["coverage_pct"] = round(actual_hours / expected_hours * 100, 1)

    return report


def clear_cache():
    """Elimina todos los archivos de caché."""
    if CACHE_DIR.exists():
        for f in CACHE_DIR.glob("*.json"):
            f.unlink()
        logger.info("Caché limpiado")
