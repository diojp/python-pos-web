from config import SQLALCHEMY_DATABASE_URI, mongodb
from flask import Flask, jsonify, request
from sqlalchemy import Integer, String, Float, Date
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
postgres = SQLAlchemy(app)

class Produtos(postgres.Model):
    id_produto = postgres.Column(Integer, primary_key = True)
    nome = postgres.Column(String)
    descricao = postgres.Column(String)
    preco = postgres.Column(Float)
    categoria = postgres.Column(String)
    def serialize(self):
        return {
            "id_produto": self.id_produto,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "categoria": self.categoria
        }

class Clientes(postgres.Model):
    id = postgres.Column(Integer, primary_key = True)
    nome = postgres.Column(String)
    email = postgres.Column(String)
    cpf = postgres.Column(String)
    data_nascimento = postgres.Column(Date)
    def serialize(self):
        return {
            "id_cliente": self.id,
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf,
            "dataNascimento": self.data_nascimento
        }

@app.route("/")
def index():
    return "<h1>Olá, mundo</h1>"

@app.route("/produtos", methods=['GET'])
def get_produtos():
    produtos = Produtos.query.all()

    return jsonify([produto.serialize() for produto in produtos])

@app.route("/produtos", methods=['POST'])
def set_produto():
    try:
        dados = request.get_json()
        produto = Produtos(
            nome=dados["nome"],
            descricao=dados["descricao"],
            preco=dados["preco"],
            categoria=dados["categoria"]
        )
        postgres.session.add(produto)
        postgres.session.commit()
        return jsonify(produto.serialize()), 201
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify(), 400

@app.route("/clientes", methods=['POST'])
def set_clientes():
    dados = request.get_json()
    cliente = Clientes(
        nome=dados["nome"],
        email=dados["email"],
        cpf=dados["cpf"],
        data_nascimento=dados["data_nascimento"]
    )
    postgres.session.add(cliente)
    postgres.session.commit()
    return jsonify(cliente.serialize()), 201

@app.route("/clientes", methods=['GET'])
def get_clientes():
    clientes = Clientes.query.all()

    return jsonify([cliente.serialize() for cliente in clientes])


if __name__ == "__main__":
    app.run(debug=True)