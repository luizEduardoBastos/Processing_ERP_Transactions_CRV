import tkinter as tk
from tkinter import filedialog
import pandas as pd


def processar_arquivo():  
    # Lista Colunas A Remover
    colunas_indesejadas = ['Tipo', 'Transferência', 'Id da Conta Financeira', 'Nome da Conta Financeira', 'Tipo de Repetiçao', 'Parcela', 'Observação/Descrição', 'Competência', 'Data Conciliação', 'Valor Previsto', 'Valor Realizado', 'Valor Rateio', 'Valor Retenção', 'Quantidade de Parcelas', 'Origem da Renegociação', 'Boleto Gerado', 'Inicial', 'Categoria', 'Departamento', 'Tipo Cliente/Fornecedor', 'Documento Cliente/Fornecedor', 'Forma de Pagamento - Parcela', 'Forma de Pagamento - Quitação', 'Numero da Nota Fiscal', 'Nome Vendedor']
    # Abrindo Janela para Selecionar Excel:
    filepath = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    # Verificando se 'Arquivo foi Selecionado' == True:
    if filepath:
        try:
            # Carregar Arquivo CSV
            df = pd.read_csv(filepath)
            # Remover Colunas Indesejadas
            df = df.drop(columns=colunas_indesejadas, errors='ignore')
            # Salvar Novo Arquivo CSV
            edited_csv_filepath = filepath.rsplit('.', 1)[0] + 'movimentações-filtradas.csv'  # Nome do novo arquivo CSV editado
            df.to_csv(edited_csv_filepath, index=False)
            # Exibindo 1ªs linhas do DF:
            result_text.insert(tk.END, df.head())
        except Exception as e:
            result_text.insert(tk.END, f"Erro ao processar arquivo: {e}")

# Criando Janela Principal:
root = tk.Tk()
root.title("Processador (Relatórios Movimentações Bom Controle")

# Botão "Processar Arquivo":
process_button = tk.Button(root, text="Selecionar arquivo e processar", command=processar_arquivo)
process_button.pack(pady=10)

# Resultado Processamento:
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

root.mainloop()