import os
import shutil
import pandas as pd
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, Toplevel
import threading  # Para rodar a atualização em uma thread separada
from service.dataframe import create_updated_dataframe, get_all_processes


# Constantes
ARQUIVO_PROCESSOS = "Processos.xlsx"
LISTA_PROCESSOS = "Lista processos.txt"


# Variáveis globais
numero_secretaria = ""
ano = ""
PLANILHA_FINAL = ""
#num_caracteres_processo = 6  # Definição inicial da variável


def selecionar_planilha():
    """Função para selecionar o arquivo de planilha, processar os dados e criar o arquivo de processos."""
    global numero_secretaria, ano

    arquivo = filedialog.askopenfilename(
        title="Selecione a planilha",
        filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
    )
    if not arquivo:
        return

    try:
        # Substituir o arquivo "Processos.xlsx"
        shutil.copy(arquivo, ARQUIVO_PROCESSOS)

        # Ler a planilha e gerar "Lista processos.txt"
        planilha = pd.read_excel(arquivo)

        # Padronizar os nomes das colunas (ignorando maiúsculas/minúsculas)
        colunas = {col.upper(): col for col in planilha.columns}
        if "OBRA" in colunas and "PROCESSO" in colunas:
            coluna_obra = colunas["OBRA"]
            coluna_processo = colunas["PROCESSO"]

            with open(LISTA_PROCESSOS, "w", encoding="utf8") as lista_processos:
                for _, row in planilha.iterrows():
                    obra = str(row[coluna_obra]).strip()
                    processo = str(row[coluna_processo]).strip()
                    lista_processos.write(f"{obra} - {processo}\n")

            messagebox.showinfo("Sucesso", "Planilha processada e arquivos atualizados!")
        else:
            messagebox.showerror("Erro", "As colunas 'OBRA' e 'PROCESSO' não foram encontradas na planilha.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar a planilha: {e}")


def abrir_planilha():
    """Função para abrir a planilha gerada."""
    if os.path.exists(PLANILHA_FINAL):
        os.startfile(PLANILHA_FINAL)  # Abre o arquivo no programa padrão
    else:
        messagebox.showerror("Erro", "A planilha final ainda não foi gerada.")


def atualizar_processos():
    """Função para rodar a atualização de processos."""
    global numero_secretaria, ano, PLANILHA_FINAL

    if not numero_secretaria or not ano:
        messagebox.showerror("Erro", "Preencha todos os campos antes de atualizar.")
        return

    # Criar uma janela de aguardo
    aguardar_janela = Toplevel(janela)
    aguardar_janela.title("Aguarde")
    aguardar_janela.geometry("300x100")
    label = Label(aguardar_janela, text="Atualizando processos. Aguarde...", font=("Arial", 12))
    label.pack(pady=20)

    # Função para rodar a atualização em uma thread separada
    def atualizar_processos_thread():
        global PLANILHA_FINAL
        try:
            # Atualiza os dados e recebe o nome do arquivo gerado
            PLANILHA_FINAL = create_updated_dataframe(numero_secretaria, ano)

            # Fechar a janela de aguardo e exibir mensagem de sucesso
            aguardar_janela.destroy()
            btn_abrir_planilha["state"] = "normal"  # Habilitar o botão de abrir planilha
            messagebox.showinfo("Sucesso", "Processos atualizados com sucesso!")
        except Exception as e:
            aguardar_janela.destroy()
            messagebox.showerror("Erro", f"Erro ao atualizar processos: {e}")

    # Rodar a função de atualização em uma thread separada
    threading.Thread(target=atualizar_processos_thread, daemon=True).start()


def definir_secretaria(event):
    """Define o número da secretaria a partir do input."""
    global numero_secretaria
    numero_secretaria = event.widget.get()


def definir_ano(event):
    """Define o ano a partir do input."""
    global ano
    ano = event.widget.get()


# Interface gráfica
janela = Tk()
janela.title("Atualizador de Processos")
janela.geometry("400x300")

Label(janela, text="Atualizador de Processos", font=("Arial", 16)).pack(pady=10)

Label(janela, text="Número da Secretaria:").pack()
entrada_secretaria = Entry(janela, justify="center")
entrada_secretaria.pack(pady=5)
entrada_secretaria.bind("<FocusOut>", definir_secretaria)

Label(janela, text="Ano:").pack()
entrada_ano = Entry(janela, justify="center")
entrada_ano.pack(pady=5)
entrada_ano.bind("<FocusOut>", definir_ano)

btn_planilha = Button(janela, text="Selecionar Planilha", command=selecionar_planilha)
btn_planilha.pack(pady=10)

btn_atualizar = Button(janela, text="Atualizar Processos", command=atualizar_processos)
btn_atualizar.pack(pady=10)

btn_abrir_planilha = Button(janela, text="Abrir Planilha Gerada", command=abrir_planilha, state="disabled")
btn_abrir_planilha.pack(pady=10)

janela.mainloop()
