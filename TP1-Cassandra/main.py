# main.py

import time
import random 
from cassandra.cluster import Cluster 

from operacoes import get_action 

# Lista de ações que o script irá executar aleatoriamente
OPTIONS = ["select_batch", "insert_batch", "delete_batch"] 

# CONFIGURAÇÃO DE CONEXÃO COM O CASSANDRA

# Mantenha os IDs das máquinas (nós/contact points) em uma lista. 
# Use o IP/nome de host do seu nó Cassandra.
ID_MAQUINA = ["127.0.0.1"] # Exemplo: Se estiver rodando localmente

# O Keyspace que você criou no Cassandra para o projeto
KEYSPACE = "reciclagem" 

def main():
    cluster = None
    session = None

    try:
        #Configurando a Conexão
        cluster = Cluster(ID_MAQUINA)
        #Conectando e Selecionando o Keyspace
        #seleciona o banco de dados 'reciclagem'.
        session = cluster.connect(KEYSPACE)
        print(f"Conexão estabelecida com o Keyspace: {KEYSPACE}")
        
        
        # O loop roda infinitamente para simular o tráfego contínuo.
        while True:
            # Escolhe uma ação aleatoriamente da lista OPTIONS
            action_type = random.choice(OPTIONS)
            
            # Chama a função principal de roteamento no arquivo actions.py
            get_action(action_type, session)
            
            # Pausa para evitar sobrecarregar o banco de dados
            
            time.sleep(1) 

    except Exception as e:
        print(f"Erro na Conexão ou Execução: {e}")

    finally:
        # Garante que a conexão seja fechada corretamente, mesmo se houver erro.
        if cluster:
            cluster.shutdown()
            print("Conexão com o Cluster Cassandra fechada.")


if __name__ == "__main__":
    main()