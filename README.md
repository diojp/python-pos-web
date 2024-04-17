# python-pos-web
#### Projeto Pyhton em MongDB e Postgres 
Disciplina Modelagem de Banco de Dados (SQL e NoSQL)
Curso de PÓS GRADUAÇÃO em Desenvolvimento Web Full Stack - UNIPÊ.

## Funcionalidades

- Projeto em Python
- Integração com Banco de Dados Postgres & MongoDB



## Instalação

Instale a biblioteca psycopg2 com o comando pip
Se faz necessário a instalação dessa biblioteca pois é um adaptador de Python para o Postgres!!!

```bash
  pip install psycopg2
```

Configure corretamente o SQLALCHEMY_DATABASE_URI para funcionar
```
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/aula_banco'
```

- Nome do Usuário do Banco = postgres;
- Password do Banco = postgres;
- Servidor = localhost;
- Porta Padrão = 5432;
- Nome do BD = aula_banco.

    

## Scripts do Banco de Dados

#### Criação das Sequences para Cliente e Produto

```sql

  CREATE SEQUENCE seq_id_cliente
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;

CREATE SEQUENCE seq_id_produto
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;
```

#### Criação das Tabelas para cliente e produto

```sql

  CREATE TABLE clientes (
	id int4 DEFAULT nextval('seq_id_cliente'::regclass) NOT NULL,
	nome varchar(255) NULL,
	email varchar(255) NULL,
	cpf varchar(11) NULL,
	data_nascimento date NULL,
	CONSTRAINT clientes_pkey PRIMARY KEY (id)
);

CREATE TABLE produtos (
	id_produto int4 DEFAULT nextval('seq_id_produto'::regclass) NOT NULL,
	nome varchar(255) NULL,
	descricao text NULL,
	preco numeric NULL,
	categoria varchar(255) NULL,
	CONSTRAINT produtos_pkey PRIMARY KEY (id_produto)
);
```

#### Populando as Tabelas para Clientes e Produtos

```sql
INSERT INTO clientes (nome,email,cpf,data_nascimento) VALUES
('Robson Junior','joaosilva@email.com','72349257899','2024-04-17'),
('Diego Magno','diego@email.com','43020254094','2024-04-18');

INSERT INTO produtos (nome,descricao,preco,categoria) VALUES
('Feijão','pacote de feijão',10.0,'NÃO PERECÍCEL'),
('SAMSUNG 60','SAMSUNG',10.0,'TV ELETRÔNICOS');
```

## Documentação da API
Acessando a API na porta padrão 5000

### CRUD Clientes

#### Retorna todos os Clientes

```http
  GET http://localhost:5000/clientes/  
```
#### Insere um Cliente

```http
  POST http://localhost:5000/cliente/
```

#### Altera / Atualiza um Cliente

```http
  PUT http://localhost:5000/cliente/${id}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. O ID do cliente que você quer atualizar |

#### Deleta / Remove um Cliente

```http
  PUT http://localhost:5000/cliente/${id}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. O ID do cliente que você quer excluir |


### CRUD Produtos

#### Retorna todos os Produtos

```http
  GET http://localhost:5000/produtos/  
```
#### Insere um Produto

```http
  POST http://localhost:5000/produto/
```

#### Altera / Atualiza um Produto

```http
  PUT http://localhost:5000/produto/${id}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. O ID do produto que você quer atualizar |

#### Deleta / Remove um Produto

```http
  PUT http://localhost:5000/produto/${id}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `int` | **Obrigatório**. O ID do produto que você quer excluir |





## Autores

- [@Diego Magno Tavares da Silva](https://www.github.com/diojp)
- [@Robson Vieira Cavalcante Júnior](https://www.github.com/diojp)

