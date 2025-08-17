import pandas as pd
import os
import time
from typing import Tuple, Optional


# Simple caching layer: write parquet (preferred) or pickle when parquet support not available.
# Cache files are stored in a `.cache` directory next to the source files.


def load_data(data_path: str = "Assignment/data.xlsx", forecast_path: str = "Assignment/Forcast.xlsx") -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """Compatibility wrapper: uses caching by default to speed up repeated loads."""
    return load_data_with_cache(data_path, forecast_path)


def _ensure_cache_dir(path: str) -> str:
    cache_dir = os.path.join(os.path.dirname(path), ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def _cache_paths_for(source_path: str) -> Tuple[str, str]:
    cache_dir = _ensure_cache_dir(source_path)
    base = os.path.splitext(os.path.basename(source_path))[0]
    return os.path.join(cache_dir, f"{base}.parquet"), os.path.join(cache_dir, f"{base}.pkl")


def _is_cache_valid(source: str, cache_file: str) -> bool:
    try:
        if not os.path.exists(cache_file) or not os.path.exists(source):
            return False
        return os.path.getmtime(cache_file) >= os.path.getmtime(source)
    except Exception:
        return False


def load_data_with_cache(data_path: str = "Assignment/data.xlsx", forecast_path: str = "Assignment/Forcast.xlsx", use_cache: bool = True) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """Load sales and forecast data with caching.

    On first run this reads Excel and writes a parquet (or pickle) cache. Subsequent calls read cache if valid.
    """
    cwd = os.getcwd()
    data_abspath = os.path.join(cwd, data_path)
    forecast_abspath = os.path.join(cwd, forecast_path)

    df_sales = None
    df_forecast = None

    # Sales
    if os.path.exists(data_abspath):
        p_parquet, p_pickle = _cache_paths_for(data_abspath)
        if use_cache and _is_cache_valid(data_abspath, p_parquet):
            try:
                df_sales = pd.read_parquet(p_parquet)
            except Exception:
                df_sales = None
        elif use_cache and _is_cache_valid(data_abspath, p_pickle):
            try:
                df_sales = pd.read_pickle(p_pickle)
            except Exception:
                df_sales = None

        if df_sales is None:
            try:
                df_sales = pd.read_excel(data_abspath)
                try:
                    df_sales.to_parquet(p_parquet, index=False)
                except Exception:
                    df_sales.to_pickle(p_pickle)
            except Exception as e:
                raise RuntimeError(f"Failed to read sales file: {e}")

    # Forecast
    if os.path.exists(forecast_abspath):
        f_parquet, f_pickle = _cache_paths_for(forecast_abspath)
        if use_cache and _is_cache_valid(forecast_abspath, f_parquet):
            try:
                df_forecast = pd.read_parquet(f_parquet)
            except Exception:
                df_forecast = None
        elif use_cache and _is_cache_valid(forecast_abspath, f_pickle):
            try:
                df_forecast = pd.read_pickle(f_pickle)
            except Exception:
                df_forecast = None

        if df_forecast is None:
            try:
                df_forecast = pd.read_excel(forecast_abspath)
                try:
                    df_forecast.to_parquet(f_parquet, index=False)
                except Exception:
                    df_forecast.to_pickle(f_pickle)
            except Exception as e:
                raise RuntimeError(f"Failed to read forecast file: {e}")

    return df_sales, df_forecast


def clear_cache(data_path: str = "Assignment/data.xlsx", forecast_path: str = "Assignment/Forcast.xlsx") -> None:
    """Remove cached files for the given source files (parquet and pickle in .cache)."""
    cwd = os.getcwd()
    data_abspath = os.path.join(cwd, data_path)
    forecast_abspath = os.path.join(cwd, forecast_path)

    for source in (data_abspath, forecast_abspath):
        cache_dir = os.path.join(os.path.dirname(source), ".cache")
        if os.path.exists(cache_dir) and os.path.isdir(cache_dir):
            try:
                base = os.path.splitext(os.path.basename(source))[0]
                for name in os.listdir(cache_dir):
                    if name.startswith(base + '.'):
                        try:
                            os.remove(os.path.join(cache_dir, name))
                        except Exception:
                            pass
            except Exception:
                pass
