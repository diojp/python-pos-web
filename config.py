from pymongo import MongoClient
# Conectando o Postgres localmente
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/aula_banco'

# Conecantando o Mongo DB local
cliente = MongoClient('mongodb://localhost:27017')
mongodb = cliente['banco_web']
pedidos_collection = mongodb['pedidos']