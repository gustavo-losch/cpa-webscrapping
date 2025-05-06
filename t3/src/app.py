from flask import Flask, request, jsonify, make_response
import csv

app = Flask(__name__)

# Define os campos (colunas) do arquivo CSV
FIELDNAMES = [
    'id', 'title', 'release_date', 'developer', 'publisher', 'genres',
    'multiplayer_or_singleplayer', 'price', 'dc_price', 'overall_review',
    'detailed_review', 'reviews', 'percent_positive',
    'win_support', 'mac_support', 'lin_support'
]

# Rota raiz apenas para verificar se o app está rodando
@app.route("/")
def index():
    return "Hello, World!"

# Rota de inserção de dados no CSV
@app.route("/insert", methods=['POST'])
def insert():
    if request.method == "POST":
        data = request.get_json()  # Recebe os dados do corpo da requisição
        with open('../games_data.csv', 'a', newline='', encoding="latin1") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writerow(data)  # Insere nova linha com os dados
        return make_response(jsonify({"message": "Inseriu um dado com sucesso!", "data": data}), 201)

# Rota de atualização de linha com base no título do jogo
@app.route("/update", methods=['PATCH'])
def update():
    if request.method == "PATCH":
        data = request.get_json()
        title = data.get("title")  # O título é usado como identificador
        if not title:
            return make_response(jsonify({"error": "Você precisa inserir um título"}), 400)

        updated_rows = []  # Lista com todas as linhas (algumas podem ser atualizadas)
        is_found = False   # Flag para saber se o título foi encontrado

        # Leitura do CSV original
        with open('../games_data.csv', 'r', newline='', encoding="latin1") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['title'] == title:
                    # Atualiza apenas os campos que fazem parte de FIELDNAMES
                    row.update({k: v for k, v in data.items() if k in FIELDNAMES})
                    is_found = True
                updated_rows.append(row)

        if not is_found:
            return make_response(jsonify({"error": "Título não encontrado!"}), 404)

        # Reescreve o CSV com os dados atualizados
        with open('../games_data.csv', 'w', newline='', encoding="latin1") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(updated_rows)

        return make_response(jsonify({"message": "Linha atualizada com sucesso!"}), 200)

# Rota para deletar uma linha com base no título do jogo
@app.route("/delete", methods=["DELETE"])
def delete():
    if request.method == "DELETE":
        data = request.get_json()
        title = data.get("title")
        if not title:
            return make_response(jsonify({"error": "Você precisa fornecer um título"}), 400)

        updated_rows = []
        is_deleted = False  # Flag que indica se foi encontrada e excluída

        with open("../games_data.csv", "r", newline='', encoding="latin1") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["title"] == title:
                    is_deleted = True
                    continue  # Ignora a linha (deletando)
                updated_rows.append(row)

        if not is_deleted:
            return make_response(jsonify({"error": "Título não encontrado!"}), 404)

        with open("../games_data.csv", "w", newline='', encoding="latin1") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(updated_rows)

        return make_response(jsonify({"message": "Linha deletada com sucesso!"}), 200)

# Rota para buscar as N primeiras linhas do CSV
@app.route("/get/<int:rows_number>", methods=['GET'])
def get(rows_number):
    if request.method == "GET":
        rows = []  # Lista com as linhas selecionadas
        with open("../games_data.csv", "r", newline='', encoding="latin1") as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i >= rows_number:  # Para ao atingir o limite solicitado
                    break
                rows.append(row)
        return make_response(jsonify(rows), 200)

# Rota para buscar linhas que tenham um valor específico na coluna 'overall_review'
@app.route("/select/<string:value>", methods=["GET"])
def select(value):
    if request.method == "GET":
        rows = []
        with open("../games_data.csv", "r", newline='', encoding="latin1") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["overall_review"] == value:  # Filtra pela coluna
                    rows.append(row)
        return make_response(jsonify(rows), 200)

# Rota para buscar por múltiplos campos simultaneamente (via JSON)
@app.route("/select_fields", methods=["GET"])
def select_fields():
    if request.method == "GET":
        data = request.get_json()  # Exemplo: {"developer": "Valve", "win_support": "True"}
        rows = []

        with open("../games_data.csv", "r", newline='', encoding="latin1") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Checa se o valor da linha é o mesmo do JSON de acordo com certa chave. Retorna True se todos os valores forem corretos.
                check = all(row.get(k) == v for k, v in data.items())
                if check:
                    rows.append(row)
        return make_response(jsonify(rows), 200)

# Inicializa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
