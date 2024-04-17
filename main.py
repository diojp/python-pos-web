from bson import ObjectId

from config import SQLALCHEMY_DATABASE_URI, mongodb, pedidos_collection
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
            "data_nascimento": self.data_nascimento
        }

class Pedidos():
    def __init__(self, id_cliente, id_produto, data_pedido, valor_pedido):
        self.id_cliente = id_cliente
        self.id_produto = id_produto
        self.data_pedido = data_pedido
        self.valor_pedido = valor_pedido

    def serialize(self):
        return {
            "id_cliente": self.id_cliente,
            "id_produto": self.id_produto,
            "data_pedido": self.data_pedido,
            "valor_pedido": self.valor_pedido
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

@app.route("/produto/<int:id>", methods=['PUT'])
def update_produto(id):
    try:
        dados = request.get_json()

        produto = postgres.session.query(Produtos).get(id)
        produto.nome = dados["nome"]
        produto.descricao = dados["descricao"]
        produto.preco = dados["preco"]
        produto.nome = dados["categoria"]

        postgres.session.commit()
        return jsonify(produto.serialize()), 201
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao alterar os dados", 400


@app.route("/produto/<int:id>", methods=['DELETE'])
def delete_produto(id):
    try:
        produto = postgres.session.query(Produtos).get(id)

        postgres.session.delete(produto)
        postgres.session.commit()
        return "Produto Excluido com Sucesso", 201
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao excluir o produto", 400

@app.route("/clientes", methods=['GET'])
def get_clientes():
    clientes = Clientes.query.all()

    return jsonify([cliente.serialize() for cliente in clientes])

@app.route("/cliente", methods=['POST'])
def set_cliente():
    try:
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
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify(), 400

@app.route("/cliente/<int:id>", methods=['PUT'])
def update_cliente(id):
    try:
        dados = request.get_json()

        cliente = postgres.session.query(Clientes).get(id)
        cliente.nome = dados["nome"]
        cliente.email = dados["email"]
        cliente.cpf = dados["cpf"]
        cliente.data_nascimento = dados["data_nascimento"]

        postgres.session.commit()
        return jsonify(cliente.serialize()), 201
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao alterar os dados", 400


@app.route("/cliente/<int:id>", methods=['DELETE'])
def delete_cliente(id):
    try:
        cliente = postgres.session.query(Clientes).get(id)

        postgres.session.delete(cliente)
        postgres.session.commit()
        return "Cliente Excluido com Sucesso", 201
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao excluir o cliente", 400

@app.route("/pedidos", methods=["GET"])
def get_pedidos():
    try:
        pedidos = pedidos_collection.find()

        # Convertendo ObjectId em strings para serialização
        pedidos_serializaveis = []
        for pedido in pedidos:
            pedido['_id'] = str(pedido['_id'])
            pedidos_serializaveis.append(pedido)

        return jsonify(pedidos_serializaveis), 200
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao listar pedidos.", 500

# Rotas para Create, Update e Delete de pedidos)
@app.route("/pedido", methods=["POST"])
def set_pedido():
    try:
        dados = request.get_json()
        novo_pedido = Pedidos(
            id_produto=dados["id_produto"],
            id_cliente=dados['id_cliente'],
            data_pedido=dados["data_pedido"],
            valor_pedido=dados["valor_pedido"]
        )
        resultado = pedidos_collection.insert_one(novo_pedido.serialize())
        if resultado.inserted_id:
            # Retorna o pedido recém-criado e o status 201
            novo_pedido.id_pedido = str(resultado.inserted_id)
            return jsonify(novo_pedido.serialize()), 201
        else:
            return "Erro ao inserir pedido.", 500
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao inserir pedido.", 400

@app.route("/pedido/<pedido_id>", methods=['DELETE'])
def delete_pedido(pedido_id):
    try:
        if not ObjectId.is_valid(pedido_id):
            return "ID de pedido inválido.", 400

        resultado = pedidos_collection.delete_one({"_id": ObjectId(pedido_id)})

        # Verifica se o pedido foi encontrado e excluído
        if resultado.deleted_count == 1:
            return (f"Pedido com ID {pedido_id} excluído com sucesso."), 200
        else:
            return (f"Pedido com ID {pedido_id} não encontrado."), 404
    except Exception as e:
        return f"Erro ao excluir pedido: {e}", 500

@app.route("/pedido/<pedido_id>", methods=["PUT"])
def update_pedido(pedido_id):
    try:
        if not ObjectId.is_valid(pedido_id):
            return "ID de pedido inválido.", 400

        # Obtém os novos dados do pedido do corpo da solicitação
        dados = request.get_json()

        # Atualiza o pedido no banco de dados
        resultado = pedidos_collection.update_one(
            {"_id": ObjectId(pedido_id)},
            {"$set": dados}  # Use $set para atualizar apenas os campos fornecidos
        )

        # Verifica se o pedido foi encontrado e atualizado
        if resultado.modified_count == 1:
            return f"Pedido com ID {pedido_id} atualizado com sucesso.", 200
        else:
            return f"Pedido com ID {pedido_id} não encontrado ou nenhum dado foi modificado.", 404
    except Exception as e:
        return f"Erro ao atualizar pedido: {e}", 500



if __name__ == "__main__":
    app.run(debug=True)