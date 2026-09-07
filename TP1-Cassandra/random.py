# utils.py

import uuid
import random

# Lista de 5 UUIDs FIXOS para simular os 5 Armazéns (Partition Keys Conhecidas)
WAREHOUSE = [
    uuid.UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'), # Armazém 1
    uuid.UUID('b1fcd345-4c0a-412f-98f6-778899aabbcc'), # Armazém 2
    uuid.UUID('c2aebc99-9c0b-4ef8-bb6d-6bb9bd380a12'), # Armazém 3
    uuid.UUID('d3fcd345-4c0a-412f-98f6-778899aabbcd'), # Armazém 4
    uuid.UUID('e4aebc99-9c0b-4ef8-bb6d-6bb9bd380a13')  # Armazém 5
]

def get_random_material_weight():
    # Retorna um peso aleatório entre 10 e 1000 kg
    return random.randint(10, 1000)

def get_random_warehouse_id():
    """Retorna um dos UUIDs de armazém definidos aleatoriamente."""
    return random.choice(WAREHOUSE)