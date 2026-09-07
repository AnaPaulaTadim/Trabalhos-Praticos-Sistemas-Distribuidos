#  SD

Os trabalhos práticos exploram diferentes conceitos relacionados à comunicação, coordenação, armazenamento e tolerância a falhas em sistemas distribuídos.

### Etapa 1 — Apache Cassandra

Inicialmente, foi desenvolvida uma aplicação utilizando o **Apache Cassandra**, um banco de dados NoSQL distribuído. O sistema simula o gerenciamento de materiais recicláveis armazenados em diferentes armazéns. Desenvolvida em Python, a aplicação realiza operações de inserção, consulta e processamento de lotes, permitindo explorar na prática a utilização de um banco de dados distribuído.

### Etapa 2 — Token Ring

Na segunda etapa, foi implementado o algoritmo **Token Ring** para controle de acesso a uma seção crítica em um sistema distribuído. Os processos são organizados logicamente em um anel, no qual um token circula entre os nós. Apenas o processo que possui o token pode acessar a seção crítica, garantindo a exclusão mútua.

A comunicação entre os processos é realizada utilizando **sockets TCP**, enquanto os nós e clientes são executados por meio de **Docker e Docker Compose**.

### Etapa 3 — Token Ring com Tolerância a Falhas

Por fim, a implementação do Token Ring foi estendida para tornar o sistema mais robusto diante de falhas. Foram incorporados mecanismos de **detecção de falhas, heartbeat, failover, transferência de estado, replicação assíncrona e armazenamento distribuído**.

Nessa etapa, o sistema é organizado em dois clusters: um responsável pela **circulação do token e atendimento das requisições**, e outro responsável pelo **armazenamento e replicação dos dados**.

Dessa forma, os trabalhos apresentam uma evolução progressiva dos conceitos de Sistemas Distribuídos, partindo do armazenamento distribuído com Apache Cassandra, passando pela coordenação e exclusão mútua com Token Ring e, posteriormente, incorporando mecanismos de tolerância a falhas e replicação.
