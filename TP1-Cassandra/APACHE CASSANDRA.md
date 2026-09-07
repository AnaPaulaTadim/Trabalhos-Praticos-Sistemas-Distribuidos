**APACHE CASSANDRA:**



Banco de Dados criados para não ter limite de armazenamento. Escrita e leitura de dados, milhares de operações por segundo um banco que nunca cai. É um banco de dados usando em grandes empresas, como Uber, Spotify,  Walmart,, IBM, Instagram, Netflix. Foi criado inicialmente por desenvolvedores do Facebook em 2007, construído especificamente para resolver um difícil problemas relacionado as pesquisas na caixa de entrada de mensagens(como lidar com diferentes volumes dados com muitas leituras e gravações aleatórias simultâneas feitas por usuários ao redor do mundo?). Disponibilizado para a comunidade opensource em 2009 e já em 2010 foi eleito top level Project pela apach Software foundation, ele vem sendo evoluído desde então por desenvolvedores de empresas como Apple, Netflix, LinkedIn, Twitter e DataStax(umas das maiores contribuidoras do Cassandra, tanto no projeto principal da open source, quanto na criação de ferramentas para seu ecossistema).

O Cassandra, um cluster Cassandra é completamente distribuído rodando em dezenas/milhares de máquinas, chamadas de \*Nós\*  simultaneamente para atender as aplicações, esta distribuição faz com que a aplicação seja tolerante a falhas de hardware e software. A distribuição também permite descentralizar a operação, não há um único ponto de falha e mesmo se houver falhas nas maquinas os dados estão sempre disponíveis. Qualquer nó do cluster consegue resolver qualquer requisição que também permite escalar um ambiente, ou seja,  se precisar armazenar mais dados, acrescente mais nós. Mas, para isso funcionar o Cassandra possui uma arquitetura que divide os dados da seguinte forma :

 	O Keyspace( que é como um contêiner de dados, semelhante a um esquema que contém várias tabelas, ele define como um conjunto de dados é replicado por data center, contendo o fator de replicação que define quantas réplicas dos dados existirão e qual será a estratégia de reaplicação dos dados, podendo ate reaplica los em diferentes data centers- boa pratica diz que devem haver pelo menos três copias dos dados distribuídos pelo cluster. A tabela que também pode ser chamada de colum Family, e que define o tipo de esquema por coleções de partições, as tabelas contem partições que contem linhas, colunas, elas conseguem adicionar novas colunas de forma flexível e sem tempo de inatividade do banco. A partição define a parte obrigatória da chave primária, que todas as linhas do cassandram devem ter para identificar um nó, em um cluster onde a linha é armazenada, por exemplo, todas as consultas fornecem a chave de partição no resultado, a linha que contém uma coleção de colunas identificadas por uma chave primária única, composta pela chave de partição e opcionalmente outras chaves de cluster e por fim a coluna que é o único dado com um tipo que pertence a uma linha. Agora como manipular tudo isso ?

 	Através de um CQL, parecido com o SQL, com ele é possível organizar dados dentro de um cluster de nós do Cassandra, podemos criar e atualizar o esquema do banco de dados e também acessar os dados, por se tratar de um banco no NoSQL as queres do Cassandra são bem mais simples que os dos bancos relacionais já que todos os dados devem ser gravados de maneira a otimizar a sua utilização pelas aplicações. O objeto principal são as tabelas que "mal comparando", se parecem com as tabelas  dos bancos relacionais, mas que possuem uma lógica de particionamento de dados que permite um alto desempenho nas operações.(ENTENDER O PARTICIONAMENTO DOS DADOS)



O apache Cassandra funciona em diversas plataformas, atráves do Linux tendo versões paras as principais distribuições, como o Ubuntu, Docker(Instalação através da imagem Docker)

 	Ex: Desenvolver uma aplicação que armazena todas as temperaturas armazenadas e coletadas por um sensor(código em cql):

 

 	CRATE TABLE temperatures\_by\_sensor(

 		sensor TEXT,

 		data DATE,

 		timestamp, TIMESTAMP,

 		value FLOAT,

 		PRIMARY KEY ((sensor, date), timestamp)) WITH CLUSTERING ORDER BY (timestamp DESC);



É comoo se cada partição fosse um arquivo com três copias gravadas em diferentes maquinas para ter alta disponibilidade. Nesse exemplo, para cada combinação de sensory date sera criado uma partição, por isso esses dois campos estão entre parêntese dentro da "primary key" isso mais os campos da segunda parte adiante são os campos de agrupamento(clusters). Alem de determinarem a unicidade dos registros eles também determinam as ordens dos registros na partição, nesse caso os dados serão ordenados pelo timestamp de maneira decrescente. Como seria uma consulta?:

 

 		SELECT sensor, data, timestamp, value

 		FROM temperatures\_by\_sensor

 		WHERE sensor = 'S001'

 			AND date = '2023-01-01'

 		LIMIT 5



Esse comando SELECT vai retornar o 5 primeiros registros mais recentes, ou seja, até a ordem de retorno dos dados é determinado junto a definição da tabela, tornando a linguagem mais simples e eficiente e memso esse sensor gerar milhares de registros por dia ainda assim buscar eesses dados sera muito rápido. Os comando de escrita de dados como INSERT, UPDATE e Delete são parecidos com o SQL



//criando novo keyspace



CREATE KEYSPACE my\_keyspace

 	WITH reaplication = {'class': 'SimpleStrategy', 'reaplication\_factor': 1};



USE my\_keyspace;



CREATE TABLE users(

 	user\_id uuid,

 	name  text,

 	email text,

 	age int,

 	PRIMARY KEY (user\_id)

);



Criamos uma nova tabela "users" com os campos, o user\_id foi definido como chave primaria, lembrando que a chave é uma combinação de colunas que são usadas para indexar e recuperar  os dados de forma eficiente.





Comando INSERT:

 

 	INSERT INTO

 		users(user\_id, name, email, age)

 	VALUES

 	(uuid(), 'Ana', 'anapaula@gmail.com',25);



INSERT e UPDATE tem os mesmo resultados no Cassandra, mesmo que um registro alvo de um update não exista ele sera criado, isso se deve ao FOCO DO CASSANDRA NA PERFORMANCE, pois ele NÃO LÊ DADOS NO MOMENTO DA ESCRITA QUE É JUSTAMENTE O QUE OS OUTROS BANCOS FAZEM. AO INVES DISSO O CASSANDRA GRAVA O NOVO VALOR POR REGISTRO NÃO IMPORTANDO SE LE ESTAVA LA ANTES AO EVITAR ESSAS LEITURAS, O CASSANDRA GANAHR PERFORMACE NAS GRAVAÇÕES DOS DADOS.





ECOSSISTEMAS DO APACHE CASSANDRA:



 	-Client Drive: que são bibliotecas que permitem que aplicativos se conectem com o Cassandra, executando operações de leitura e gravação.

 	-Clusters Manage: que são ferramentas de gerenciamento de cluster que simplificam a implantação e monitoramento de clusters.

 	-DateStax OpsCenter: gerenciamento e monitoramento visual, fácil de usar, para clusters data stacks, com ele é possível monitorar, fazer backup, restauração  e gerenciar clusters DSE.





 

IDEIA DO BANCO DE DADOS:



-RESERVA DE ESTOQUE DE RECICLAGEM:

Como o Cassandra trabalha com o modelo de colunas estendidas, cada coluna vai representar o tipo do material reciclável(metal, plástico, papel ou vidro), onde cada coluna vai ser identificada com uma chave de partição, para acessar cada coluna, 









