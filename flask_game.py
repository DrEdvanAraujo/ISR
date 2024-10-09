from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import webbrowser

app = Flask(__name__)
app.config["SECRET_KEY"] = "sua_chave_secreta"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

perguntas = [
    {"pergunta": "Tosse menor que 2 semanas?", "pontos": 0},
    {"pergunta": "Tosse entre 2 a 3 semanas?", "pontos": 1},
    {"pergunta": "Tosse maior que 3 semanas?", "pontos": 2},
    {"pergunta": "Expectoração/catarro com sangue?", "pontos": 1},
    {"pergunta": "Febre persistente?", "pontos": 1},
    {"pergunta": "Perda de peso?", "pontos": 1},
    {"pergunta": "Suor noturno?", "pontos": 1},
    {"pergunta": "Fuma/Histórico de alcoolismo ou uso de drogas?", "pontos": 1},
    {"pergunta": "Possui Diagnóstico de Diabetes, Doença Pulmonar ou Doença do Sistema Imunológico?", "pontos": 1},
    {"pergunta": "Portador de HIV?", "pontos": 1},
    {"pergunta": "Contato com paciente diagnosticado com tuberculose?", "pontos": 1},
    {"pergunta": "Já teve diagnóstico prévio de TB?", "pontos": 1},
    {"pergunta": "Realizou tratamento prévio para TB?", "pontos": 1},
    {"pergunta": "Pessoa em situação de rua?", "pontos": 1},
    {"pergunta": "Pessoa em situação privada de liberdade (ou histórico até 06 meses)?", "pontos": 1},
    {"pergunta": "Uso de medicamento imunossupressor (quimioterapia, corticoterapia prolongada)?", "pontos": 1}
]

@app.route("/")
def inicio():
    session["indice_atual"] = 0
    session["pontos"] = 0
    session["respostas"] = [None] * len(perguntas)
    return render_template("index.html")

@app.route("/pergunta", methods=["GET", "POST"])
def pergunta():
    if request.method == "POST":
        resposta = request.form.get("resposta")
        indice_atual = session["indice_atual"]

        # Ajusta a pontuação ao mudar resposta
        if session["respostas"][indice_atual] == "sim":
            session["pontos"] -= perguntas[indice_atual]["pontos"]

        session["respostas"][indice_atual] = resposta
        if resposta == "sim":
            session["pontos"] += perguntas[indice_atual]["pontos"]

        session["indice_atual"] += 1

        if session["indice_atual"] >= len(perguntas):
            return redirect(url_for("resultado"))

    indice_atual = session["indice_atual"]
    pergunta_atual = perguntas[indice_atual]["pergunta"]
    return render_template("pergunta.html", pergunta=pergunta_atual, indice=indice_atual)

@app.route("/voltar", methods=["POST"])
def voltar():
    if session["indice_atual"] > 0:
        session["indice_atual"] -= 1
        if session["respostas"][session["indice_atual"]] == "sim":
            session["pontos"] -= perguntas[session["indice_atual"]]["pontos"]

        session["respostas"][session["indice_atual"]] = None

    return redirect(url_for("pergunta"))

@app.route("/resultado")
def resultado():
    pontos = session["pontos"]
    if pontos >= 2:
        mensagem_final = (
            "Indicação de realizar o TRM-TB!<br>"
            "Orientação: Registrar o paciente no livro de sintomático respiratório."
        )
        link = "https://drive.google.com/file/d/1ksM8A91GIUWQOPha6qE460yOJr3X_Wme/view?usp=sharing"
    else:
        mensagem_final = "Sem indicação de realizar o TRM-TB."
        link = None

    return render_template("resultado.html", resultado=mensagem_final, link=link)

if __name__ == "__main__":
    app.run(debug=True)
