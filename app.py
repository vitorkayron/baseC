from flask import Flask, jsonify, request, render_template
import requests


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar_cpf', methods=['GET'])
def buscar_cpf():
    cpf = request.args.get('cpf')
    if not cpf:
        return jsonify({'erro': 'CPF não existe em nosso banco de dados.'}), 400

    usuario = request.args.get('usuario')
    senha = request.args.get('senha')
    if not usuario or not senha:
        return jsonify({'erro': 'Usuário ou senha inválidos.'}), 401

    url = f'http://localhost:8000/api/v1/baseB?cpf={cpf}'
    response = requests.get(url, auth=(usuario, senha))
    if response.status_code != 200:
        return jsonify({'erro': 'Usuário ou senha incorreto.'}), 500
    elif response.status_code == 404:
        return jsonify({'erro': 'CPF não encontrado na base de dados.'}), 404

    clientes = response.json().get('results')
    if not clientes:
        return jsonify({'erro': 'CPF não encontrado na base de dados.'}), 404

    cliente = clientes[0]
    return jsonify({
        'cpf': cliente['cpf'],
        'nome': cliente['nome'],
        'ultima_consulta': cliente['ultima_consulta'],
        'movimentacao_financeira': cliente['movimentacao_financeira']
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)