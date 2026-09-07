import os
import time

CLUSTER_SIZE = 5

def get_timestamp() -> int:
    """Retorna timestamp atual em milissegundos."""
    return int(time.time() * 1000)

def get_env_var(key: str, default_val: str) -> str:
    """Lê variável de ambiente com fallback para valor padrão."""
    return os.environ.get(key, default_val)
