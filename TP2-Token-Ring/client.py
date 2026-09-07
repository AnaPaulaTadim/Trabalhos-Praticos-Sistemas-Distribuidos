"""
client.py — Cliente do Cluster Sync

Cada cliente envia entre 10 e 50 pedidos de acesso ao recurso R,
aguardando a resposta COMMITTED antes de esperar e re-tentar.
"""

import socket
import time
import random
import sys

from utils import get_timestamp, get_env_var

def main() -> None:
    random.seed()

    MEU_ID   = int(get_env_var("CLIENT_ID",        "100"))
    NODE_HOST = get_env_var("TARGET_NODE_HOST", "127.0.0.1")
    NODE_PORT = int(get_env_var("TARGET_NODE_PORT",  "8080"))

    total_acessos = 9 + random.randint(1, 41)   # 10–50 acessos
    print(f"[CLIENTE {MEU_ID} INICIADO] {total_acessos} acessos ao recurso R.")
    sys.stdout.flush()

    i = 1
    while i <= total_acessos:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((NODE_HOST, NODE_PORT))

            ts  = get_timestamp()
            msg = f"{MEU_ID}|{ts}"
            sock.sendall(msg.encode())

            # Bloqueia aguardando COMMITTED
            response = sock.recv(1024).decode().strip()
            if response == "COMMITTED":
                print(f"[{i}/{total_acessos}] Acesso Confirmado: {response}")
            else:
                print(f"Resposta inesperada: {response}", file=sys.stderr)

            sock.close()
            i += 1  # só avança quando bem-sucedido

        except OSError:
            print(
                f"[FALHA] Não foi possível conectar ao nó {NODE_HOST}. "
                "Tentando novamente no próximo ciclo.",
                file=sys.stderr,
            )
            # i não avança — nova tentativa no próximo ciclo

        espera = 1 + random.randint(0, 4)   # Sleep 1–5 s
        sys.stdout.flush()
        time.sleep(espera)

    print(f"[CLIENTE FINALIZADO] {MEU_ID} finalizou todos os acessos programados.")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
