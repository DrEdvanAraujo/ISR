from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Perguntas e Pontuação
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

# Variáveis globais para controlar o progresso
pontuacao = 0
indice_atual = 0

@app.route('/')
def inicio():
    global pontuacao, indice_atual
    pontuacao = 0
    indice_atual = 0
    return render_template('index.html')

@app.route('/perguntas', methods=['GET', 'POST'])
def perguntas_func():
    global pontuacao, indice_atual

    if request.method == 'POST':
        resposta = request.form['resposta']
        if resposta == 'sim':
            pontuacao += perguntas[indice_atual]["pontos"]
        indice_atual += 1

    if indice_atual < len(perguntas):
        pergunta_atual = perguntas[indice_atual]["pergunta"]
        return render_template('perguntas.html', pergunta=pergunta_atual)
    else:
        return redirect(url_for('resultado'))

@app.route('/resultado')
def resultado():
    if pontuacao >= 2:
        resultado = "Indicação de realizar o TRM-TB! Registrar o paciente no livro de sintomático respiratório."
        link = "https://drive.google.com/file/d/1ksM8A91GIUWQOPha6qE460yOJr3X_Wme/view?usp=sharing"
        video_coleta_link = "https://www.youtube.com/embed/ZQ3g1Llh1Mw"
    else:
        resultado = "Sem indicação de realizar o TRM-TB."
        link = None
        video_coleta_link = None
    return render_template('resultado.html', resultado=resultado, link=link, video_coleta_link=video_coleta_link)

if __name__ == "__main__":
    app.run(debug=True)
