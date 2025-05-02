#Fazendo operaçoes CRUD sem usar pandas, apenas via csv

from flask import Flask, request, jsonify
#from flask_cors import CORS
import csv

app = Flask(__name__)
#CORS(app)
app.config.from_mapping(
    SECRET_KEY="dev",
)
app.config.from_prefixed_env()

@app.route("/")
def index():
    return "Hello, World!"

FIELDNAMES = ['title','release_date','developer','publisher','genres','multiplayer_or_singleplayer','price','dc_price','overall_review','detailed_review','reviews','percent_positive','win_support','mac_support','lin_support']

@app.route("/insert", methods=['POST'])
def insert():
    data = request.get_json()
    with open('clean_data.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(data)
    return jsonify({"message": "Inseriu um dado com sucesso!", "data": data})

@app.route("/update", methods=['PATCH'])
def update():
    data = request.get_json()
    title = data["title"]
    if not title:
        return {"error": "Voce precisa inserir um titulo"}, 400

    updated_rows = []
    is_found = False
    with open('clean_data.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['title'] == title:
                row.update(data)  ##buil-in python dicionarios para atualizar!
                is_found = True
            updated_rows.append(row)

    if not is_found:
        return {"error": "Titulo nao encontrado!."}, 404

    with open('clean_data.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(updated_rows)
        file.close()
    return {"message": "Linha ataulizada com sucesso!."}, 200

@app.route("/delete", methods=["DELETE"])
def delete():
    data = request.get_json()
    title = data["title"]
    if not title:
        return {"error": "Você precisa fornecer um título"}, 400

    updated_rows = []
    is_deleted = False

    with open("clean_data.csv", "r", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["title"] == title:
                is_deleted = True
                continue  # pula essa linha (deletando)
            updated_rows.append(row)

    if not is_deleted:
        return {"error": "Título não encontrado!"}, 404

    with open("clean_data.csv", "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(updated_rows)

    return {"message": "Linha deletada com sucesso!"}, 200

@app.route("/get/<int:rows_number>", methods=['GET'])
def get(rows_number):
    rows = []
    with open("clean_data.csv", "r", newline='') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader): #itera pelo iterator ( next(reader) etc .. ) 
            if i >= rows_number:
                break    
            rows.append(row)
    return jsonify(rows)

@app.route("/select/<string:value>", methods=["GET"]) # para a coluna 'overall_review'
def select(value):
    rows = []
    with open("clean_data.csv", "r", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["overall_review"] == value:
                rows.append(row)
    return jsonify(rows)

@app.route("/select_fields", methods=["GET"]) #aqui sera passado um json
def select_fields():
    data = request.get_json()
    print(data)
    rows = []
    with open("clean_data.csv", "r", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            check = True
            for key in data:
                if data[key] != row[key]:
                    check = False
                    break
            if check:
                rows.append(row)
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)