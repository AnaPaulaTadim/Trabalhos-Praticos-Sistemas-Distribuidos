FROM python:3.12-slim

WORKDIR /app

# Copia apenas os arquivos Python necessários
COPY utils.py   .
COPY node.py    .
COPY client.py  .

RUN mkdir -p /app/data

# Por padrão inicia o nó; clientes sobrescrevem com `command:`
CMD ["python", "-u", "node.py"]
