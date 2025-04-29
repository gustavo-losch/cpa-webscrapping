from flask import Flask, request, make_response, jsonify, abort
import requests

print(__name__)
app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello world.</h1>"

# Id: index da lista
tasklist = []

# Cria uma rota para tarefas aceitando os metodos GET e POST
@app.route("/tasks", methods=["GET", "POST"])
def task():

    # Método para GET
    if request.method == "GET":
        return make_response(jsonify(tasklist))
    
    # Método para POST
    elif request.method == "POST":
        dados = request.get_json()
        nova_tarefa = dados["tarefa"]
        if nova_tarefa not in tasklist:
            tasklist.append(tasklist)
            return make_response(jsonify("Tarefa inserida com sucesso"), 200)
        else:
            return make_response(jsonify("Tarefa já está na lista!"), 400)
    
    # Se não, 404
    else:
        abort(404)


@app.route("/task/<int:id>", methods=["GET", "PUT", "DELETE"])
def task(id):
    if id >= len(tasklist):
        return make_response(jsonify("Tarefa não existe."), 400)
    
    else:
        if request.method == "GET":
            return make_response(jsonify(tasklist))
        
        elif request.method == "PUT":
            dados = request.get_json()
            edited_task = dados["tarefa"]
            tasklist[id] = edited_task
            return make_response(jsonify("Tarefa editada com sucesso."), 200)
        
        elif request.method == "DELETE":
            tasklist.pop(id)
            return make_response(jsonify("Tarefa removida com sucesso"), 200)

        else:
            abort(404)

if __name__ == "__main__":
    app.run(debug=True)