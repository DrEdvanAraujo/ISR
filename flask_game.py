import tkinter as tk
from tkinter import messagebox
import webbrowser

class TRMTBJogo:
    def __init__(self, root):
        self.root = root
        self.root.title("Investigação de Paciente Sintomático Respiratório")
        self.root.geometry("450x400")
        self.video_link = "https://youtu.be/bIZqLj7kjXQ"

        # Botões de vídeo
        self.button_video = tk.Button(root, text="Assistir ao vídeo de introdução", command=self.abrir_video)
        self.button_video.pack(pady=10)

        self.button_pular_video = tk.Button(root, text="Pular vídeo", command=self.iniciar_jogo)
        self.button_pular_video.pack(pady=10)

    def abrir_video(self):
        webbrowser.open(self.video_link)
        self.iniciar_jogo()

    def iniciar_jogo(self):
        self.button_video.pack_forget()
        self.button_pular_video.pack_forget()

        self.perguntas = [
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
        self.indice_atual = 0
        self.pontos = 0
        self.respostas = [None] * len(self.perguntas)

        self.label_titulo = tk.Label(self.root, text="Jogo de Avaliação para TRM-TB", font=("Helvetica", 16))
        self.label_titulo.pack(pady=10)

        self.label_pergunta = tk.Label(self.root, text="")
        self.label_pergunta.pack(pady=10)

        self.button_sim = tk.Button(self.root, text="Sim", command=lambda: self.responder("sim"))
        self.button_sim.pack(side=tk.LEFT, padx=20, pady=10)

        self.button_nao = tk.Button(self.root, text="Não", command=lambda: self.responder("nao"))
        self.button_nao.pack(side=tk.LEFT, padx=20, pady=10)

        self.button_voltar = tk.Button(self.root, text="Voltar", command=self.voltar_pergunta)
        self.button_voltar.pack(side=tk.RIGHT, padx=20, pady=10)

        self.mostrar_pergunta()

    def mostrar_pergunta(self):
        pergunta_atual = self.perguntas[self.indice_atual]["pergunta"]
        self.label_pergunta.config(text=pergunta_atual)

    def responder(self, resposta):
        self.respostas[self.indice_atual] = resposta
        if resposta == "sim":
            self.pontos += self.perguntas[self.indice_atual]["pontos"]
        self.indice_atual += 1

        if self.indice_atual < len(self.perguntas):
            self.mostrar_pergunta()
        else:
            self.finalizar_jogo()

    def voltar_pergunta(self):
        if self.indice_atual > 0:
            # Se a resposta anterior foi "sim", subtrair os pontos ao voltar
            if self.respostas[self.indice_atual - 1] == "sim":
                self.pontos -= self.perguntas[self.indice_atual - 1]["pontos"]
            self.indice_atual -= 1
            self.mostrar_pergunta()

    def finalizar_jogo(self):
        if self.pontos >= 2:
            mensagem_final = (
                "Indicação de realizar o TRM-TB!\n"
                "Orientação: Registrar o paciente no livro de sintomático respiratório."
            )
            messagebox.showinfo("Resultado", mensagem_final)
            webbrowser.open("https://drive.google.com/file/d/1ksM8A91GIUWQOPha6qE460yOJr3X_Wme/view?usp=sharing")
        else:
            mensagem_final = "Sem indicação de realizar o TRM-TB."
            messagebox.showinfo("Resultado", mensagem_final)

        self.opcoes_finais()

    def opcoes_finais(self):
        opcao = messagebox.askyesno("Finalizado", "Deseja assistir ao vídeo com instruções para coleta do escarro? Clique em 'Não' para reiniciar o questionário.")
        if opcao:
            webbrowser.open("https://youtu.be/ZQ3g1Llh1Mw?si=jwT5OO5oJRy71Gea")
        else:
            self.reiniciar_jogo()

    def reiniciar_jogo(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    jogo = TRMTBJogo(root)
    root.mainloop()
