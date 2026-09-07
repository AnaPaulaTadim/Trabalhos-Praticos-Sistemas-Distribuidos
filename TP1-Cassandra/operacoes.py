#Operações dentro do banco de dados(inserir, vizualizar e deletar)


from cassandra.query import SimpleStatement 
from cassandra.utils import uuid_from time 
from cassandra.utils import get_random_material_weigth

from random import get_random_warehouse_id, get_random_material_weight

# Definição das colunas de material (necessário para a função de DELETE)
MATERIAL_COLUMNS = [
    'metal_kg', 
    'plastic_kg', 
    'paper_kg', 
    'glass_kg', 
    'electronic_kg'
]

#Função para rotear as chamadas 
def get_action(action, session):

    actions = {
        "select_batch" : select_batch,
        "insert_batch" : insert_batch,
        "delete_batch" : delete_batch
    }

#Função pra gravar um novo item 
def insert_batch(session):

    #Selecionando aleatoriamente um dos 5 armazens
    warehouse_id = get_random_warehouse()

    #Gera um novo ID em tempo real
    batch_id = uuid_from_time(time=None) 
    #gera pesos aleatórios para cada material
    metal = get_random_material_weight()
    plastic = get_random_material_weight()
    paper = get_random_material_weight()
    glass = get_random_material_weight()
    eletronics = get_random_material_weight()

     
    #%s sao os "buracos" para onde esses valores vao 
    #mostrando onde os valores vao ser inseridos 
    cql = """
    INSERT INTO waste_stock (warehouse_id, batch_id, metal_kg, plastic_kg, paper_kg, glass_kg)
    VALUES (%s, %s, %s, %s, %s, %s) 
    """
    #Preenche os buracos com os dados e envia para o Cassandra
    session.execute(cql, (warehouse, batch_id, metal, plastic, paper, glass))
    print(f"INSERT: Novo lote (ID: {batch_id}) adicionado ao Armazém: {warehouse}")

#Busca por materiais ja inseridos em um Armazém 
def select_batch(session):

    #Seleciona aleatoriamente um dos 5 armazens 
    warehouse_to_query = get_random_warehouse_id()

    #Busca dentro do armazem seleiconado o intem que deseja consultar 
    cql = """
    SELECT warehouse_id, batch_id, metal_kg, plastic_kg, paper_kg, glass_kg 
    FROM waste_stock 
    WHERE warehouse_id = %s
    LIMIT 5
    """

    try:

        #Executa a query no Cassandra 
        rows = session.execute(cql, (warehouse_to_query,))

        #Mostra qual armazem esta sendo consultado 
        print(f"SELECT: Resultados de Reciclagem para Armazém: {warehouse_to_query}")

        #Caso não haja registros, retorna vazio 
        if not rows:
             print("Nenhum lote encontrado neste armazém.")
             return

        #Mostrando resultados encontrados 
        for row in rows:
        print(f"Lote ID: {row.batch_id}")
        print(f"  > Metal: {row.metal_kg} kg | Plástico: {row.plastic_kg} kg")
        print(f"  > Papel: {row.paper_kg} kg | Vidro: {row.glass_kg} kg | Eletrônico: {row.electronic_kg} kg")

        #se houver erro na consulta 
    except Exception as e:
        print(f"ERRO item não encontrado: {e}")


def delete_batch(session):

    #Seleciona aleatoriamente um dos 5 armazens 
    Encontra um lote (batch_id) existente e todos os seus pesos nesse armazém.
    select_cql = f"""
    SELECT batch_id, {', '.join(MATERIAL_COLUMNS)}
    FROM waste_stock
    WHERE warehouse_id = %s
    LIMIT 1
    """

    try:
        # Executa o SELECT para obter o ID e os pesos do lote
        rows = session.execute(select_cql, (warehouse_id_to_find,))
        
        if not rows:
            print(f"PROCESS: Armazém {warehouse_id_to_find} está vazio. Nada para processar.")
            return

        # Extrai os dados do lote (apenas o primeiro resultado)
        row_data = rows.one()
        batch_to_update = row_data.batch_id
        
        # 3. Escolhe aleatoriamente um material para processar
        material_to_process = random.choice(MATERIAL_COLUMNS)
        existing_weight = getattr(row_data, material_to_process) # Pega o valor da coluna dinamicamente
        
        # Gera uma quantidade aleatória para remover (simulando o processamento)
        quantity_to_remove = random.randint(10, 500)

        # 4. Lógica Condicional para o UPDATE
        if existing_weight > quantity_to_remove:
            # Caso 1: Tem mais material do que precisa ser removido
            new_weight = existing_weight - quantity_to_remove
            log_msg = f"Reduzido {quantity_to_remove}kg. Novo peso: {new_weight}kg."
        else:
            # Caso 2: Quantidade a remover é maior ou igual ao disponível
            new_weight = 0
            quantity_to_remove = existing_weight # Ajusta a mensagem para o que realmente foi removido
            log_msg = f"Removido todo o estoque de {quantity_to_remove}kg. Peso zerado."
            
        
        # 5. Constrói e executa o comando UPDATE (usando o nome da coluna dinamicamente)
        update_cql = f"""
        UPDATE waste_stock 
        SET {material_to_process} = %s 
        WHERE warehouse_id = %s AND batch_id = %s
        """

        session.execute(update_cql, (new_weight, warehouse_id_to_find, batch_to_update))
        
        
        print(f"PROCESSAMENTO: Lote {batch_to_update} no Armazém {warehouse_id_to_find}")
        print(f"Material processado: {material_to_process.upper()}")
        print(f"Ação: {log_msg}")
        

    except Exception as e:
        print(f" ERRO ao processar lote: {e}")

