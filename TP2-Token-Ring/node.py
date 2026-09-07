"""
node.py — Nó do Cluster Sync (Protocolo de Exclusão Mútua por Token Ring)

Cada nó escuta clientes na porta 8080 e troca o token com o próximo
nó do anel na porta 9090. O token é um vetor JSON de CLUSTER_SIZE entradas.
"""

import os
import sys
import socket
import threading
import time
import random
import json
import fcntl
from queue import Queue, Empty

from utils import CLUSTER_SIZE, get_timestamp, get_env_var

# ---------------------------------------------------------------------------
# Estado global
# ---------------------------------------------------------------------------
fila_pedidos: Queue = Queue()
lock = threading.Lock()

token: list = [{"node_id": i, "timestamp": -1, "client_id": -1}
               for i in range(CLUSTER_SIZE)]

MEU_ID: int = -1
PROXIMO_HOST: str = ""

# ---------------------------------------------------------------------------
# Seção Crítica
# ---------------------------------------------------------------------------
def acessar_recurso(c_id: int, c_timestamp: int) -> None:
    print(f"\n[SESSÃO CRÍTICA] Nó {MEU_ID} atendendo Cliente {c_id} está acessando o recurso.")
    sys.stdout.flush()
    os.makedirs("/app/data", exist_ok=True)
    with open("/app/data/log_recurso.txt", "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(f"Nó {MEU_ID} escreveu para Cliente {c_id} às {c_timestamp}\n")
        f.flush()
        time.sleep((200 + random.randint(0, 800)) / 1000)
        fcntl.flock(f, fcntl.LOCK_UN)

# ---------------------------------------------------------------------------
# Helpers de rede
# ---------------------------------------------------------------------------
def recv_all(conn: socket.socket) -> bytes:
    """Recebe dados até o socket fechar (EOF)."""
    data = b""
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

def enviar_token(host: str, token_data: list) -> None:
    """Envia o token serializado como JSON para o próximo nó, com retry."""
    payload = json.dumps(token_data).encode()
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, 9090))
            s.sendall(payload)
            s.close()
            return
        except OSError:
            time.sleep(1)

# ---------------------------------------------------------------------------
# Thread: Anel de Tokens (porta 9090)
# ---------------------------------------------------------------------------
def thread_anel() -> None:
    global token

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", 9090))
    server.listen(10)

    # Nó 0 injeta o token inicial após aguardar os vizinhos subirem
    if MEU_ID == 0:
        print("[NÓ 0] Aguardando vizinhos inicializarem (10s)...")
        sys.stdout.flush()
        time.sleep(10)
        token = [{"node_id": i, "timestamp": -1, "client_id": -1}
                 for i in range(CLUSTER_SIZE)]
        enviar_token(PROXIMO_HOST, token)

    pedido_atual: dict = {"socket": None, "client_id": -1}

    while True:
        # Aguarda chegada do token
        conn, _ = server.accept()
        data = recv_all(conn)
        conn.close()

        token = json.loads(data.decode())

        print(f"\n\n===== NÓ {MEU_ID} VERIFICANDO O TOKEN... =====")
        print("\nTOKEN:")
        for entry in token:
            print(f"NO [{entry['node_id']}] | CLIENT_ID = {entry['client_id']} | TIMESTAMP = {entry['timestamp']}")
        sys.stdout.flush()

        with lock:
            # --- FASE 1: meu pedido percorreu o anel — verificar prioridade ---
            if token[MEU_ID]["timestamp"] != -1:
                sou_o_menor = True
                for i in range(CLUSTER_SIZE):
                    t_i = token[i]["timestamp"]
                    t_eu = token[MEU_ID]["timestamp"]
                    if t_i != -1 and (t_i < t_eu or (t_i == t_eu and i < MEU_ID)):
                        sou_o_menor = False
                        break

                if sou_o_menor:
                    acessar_recurso(pedido_atual["client_id"], get_timestamp())
                    # Responde COMMITTED ao cliente
                    try:
                        pedido_atual["socket"].sendall(b"COMMITTED")
                        pedido_atual["socket"].close()
                    except OSError:
                        pass
                    # Limpa posição no token (NULL)
                    token[MEU_ID]["timestamp"] = -1
                    token[MEU_ID]["client_id"] = -1
                    pedido_atual = {"socket": None, "client_id": -1}

            # --- FASE 2: nó livre com pedido na fila — registra no token ---
            if token[MEU_ID]["timestamp"] == -1:
                try:
                    r = fila_pedidos.get_nowait()
                    token[MEU_ID]["timestamp"] = r["timestamp"]
                    token[MEU_ID]["client_id"] = r["client_id"]
                    pedido_atual = {"socket": r["socket"], "client_id": r["client_id"]}
                except Empty:
                    pass

        # Controle de vazão antes de repassar o token
        time.sleep(1)
        enviar_token(PROXIMO_HOST, token)

# ---------------------------------------------------------------------------
# Thread: Atendimento de Clientes (porta 8080)
# ---------------------------------------------------------------------------
def thread_cliente() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", 8080))
    server.listen(10)

    while True:
        cli, _ = server.accept()
        data = cli.recv(1024).decode().strip()
        if "|" in data:
            parts = data.split("|")
            cid = int(parts[0])
            ts = int(parts[1])
            with lock:
                fila_pedidos.put({"socket": cli, "client_id": cid, "timestamp": ts})
            print(f"\n [NOVO PEDIDO] Cliente {cid} (TS: {ts})")
            sys.stdout.flush()

# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    MEU_ID = int(get_env_var("MY_ID", "0"))
    PROXIMO_HOST = get_env_var("NEXT_NODE_HOST", "node0")

    print(f"\n[INICIANDO CLUSTER] Iniciando nó {MEU_ID} (Próximo Nó: {PROXIMO_HOST})")
    sys.stdout.flush()

    t1 = threading.Thread(target=thread_cliente, daemon=True, name="thread-cliente")
    t2 = threading.Thread(target=thread_anel, daemon=True, name="thread-anel")
    t1.start()
    t2.start()
    t1.join()
    t2.join()
