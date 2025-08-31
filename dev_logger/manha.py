import tkinter as tk
from tkinter import ttk
import tkcalendar
import datetime
import json

class JanelaMeta:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Metas")

        # Calendário
        self.calendar = tk.Frame(self.root)
        self.calendar.pack(pady=20)
        self.cal = tkcalendar.Calendar(self.calendar, selectmode='day', year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        self.cal.pack()

        # Botões de seleção de data e relatório
        self.botao_selecionar_data = tk.Button(self.root, text="Selecionar Data", command=self.selecionar_data)
        self.botao_selecionar_data.pack(pady=10)

        self.toplevel_relatorio = None

    def selecionar_data(self):
        # Salva a data escolhida em memório
        self.data_escolhida = self.cal.selection_get()
        
        # Ativa os botões de relatório e narrativa
        self.botao_selecionar_data.config(state="disabled")
        self.botao_relatorio = tk.Button(self.root, text="Relatório", command=self.abrir_toplevel_relatorio)
        self.botao_relatorio.pack(pady=10)
        self.botao_narrativa = tk.Button(self.root, text="Narrativa", command=lambda: print("Narrativa"))
        self.botao_narrativa.pack(pady=10)

    def abrir_toplevel_relatorio(self):
    # Abre a janela toplevel para relatório
        self.toplevel_relatorio = tk.Toplevel()
        self.toplevel_relatorio.title(f"Relatório da data {self.data_escolhida}")

        # Configura a janela toplevel
        self.toplevel_relatorio.geometry("800x600")  # Define a largura e altura da janela
        self.toplevel_relatorio.resizable(True, True)  # Deixa a janela redimensionável
        self.toplevel_relatorio.minsize(800, 600)  # Define o tamanho mínimo da janela
        self.toplevel_relatorio.maxsize(1200, 900)  # Define o tamanho máximo da janela

        # Perguntas do relatório
        self.pergunta_repetir = tk.Label(self.toplevel_relatorio, text="O que fiz ontem que preciso repetir:")
        self.pergunta_repetir.grid(row=0, column=0, padx=10, pady=5)
        self.resposta_repetir = tk.Text(self.toplevel_relatorio, height=5, width=50)
        self.resposta_repetir.grid(row=0, column=1, padx=10, pady=5)

        self.pergunta_nao_fazer = tk.Label(self.toplevel_relatorio, text="O que fiz ontem que tenho que parar de fazer:")
        self.pergunta_nao_fazer.grid(row=1, column=0, padx=10, pady=5)
        self.resposta_nao_fazer = tk.Text(self.toplevel_relatorio, height=5, width=50)
        self.resposta_nao_fazer.grid(row=1, column=1, padx=10, pady=5)

        self.pergunta_habito = tk.Label(self.toplevel_relatorio, text="O que fiz ontem que tem que virar hábito:")
        self.pergunta_habito.grid(row=2, column=0, padx=10, pady=5)
        self.resposta_habito = tk.Text(self.toplevel_relatorio, height=5, width=50)
        self.resposta_habito.grid(row=2, column=1, padx=10, pady=5)

        self.grande_vitoria = tk.Label(self.toplevel_relatorio, text="Qual a única coisa que posso fazer hoje que deixa todas as outras mais fáceis e irrelevantes:")
        self.grande_vitoria.grid(row=3, column=0, padx=10, pady=5)
        self.resposta_grande_vitoria = tk.Text(self.toplevel_relatorio, height=5, width=50)
        self.resposta_grande_vitoria.grid(row=3, column=1, padx=10, pady=5)

        self.botao_salvar_dados = tk.Button(self.toplevel_relatorio, text="Salvar Dados", command=self.salvar_dados)
        self.botao_salvar_dados.grid(row=4, column=0, columnspan=2, pady=10)


    def salvar_dados(self):
        # Salva os dados em um arquivo JSON
        data = {
            "data": str(self.data_escolhida),
            "repetir": self.resposta_repetir.get("1.0", tk.END),
            "parar_fazer": self.resposta_nao_fazer.get("1.0", tk.END),
            "habito": self.resposta_habito.get("1.0", tk.END),
            "grande_vitoria": self.resposta_grande_vitoria.get("1.0", tk.END)
        }
        
        # Salva os dados em um arquivo

        
        # Salva os dados em um arquivo JSON
        with open(f"relatorio_{self.data_escolhida}.json", "w") as f:
            json.dump(data, f)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = JanelaMeta()
    app.run()
