from flask import Flask, render_template, request, jsonify
from analising import classificar_email
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analisar', methods=['POST'])
def analisar():
    try:
        dados = request.get_json()
        
        if not dados or 'texto' not in dados:
            return jsonify({'erro': 'Nenhum texto foi recebido.'}), 400
        
        texto_para_analisar = dados['texto']

        if not texto_para_analisar.strip():
            return jsonify({'erro': 'O texto está vazio.'}), 400

        categoria, resposta = classificar_email(texto_para_analisar)

        return jsonify({
            'categoria': categoria,
            'resposta': resposta
        })

    except Exception as e:
        # Se der qualquer erro no servidor, avisa o front sem travar tudo
        print(f"Erro no servidor: {e}")
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)