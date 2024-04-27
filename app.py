import tkinter as tk, pandas as pd
from tkinter import filedialog


def print_error(result_text, message):
    result_text.insert(tk.END, message)

def process_file(filepath, colunas_indesejadas):  
    try:
        if not filepath.lower().endswith(".csv"):
            return "O arquivo não é um CSV."
        df = pd.read_csv(filepath) # Loading CSV
        # Remove Unwanted Columns
        df = df.drop(columns=colunas_indesejadas, errors='ignore') # Remover Colunas Indesejadas
        df = df.astype(str) # All Cells to String
        # Replace Specified Characters in All Cells
        for coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda cell: cell.replace('ã', 'a').replace('Ã', 'A').replace('õ', 'o').replace('Õ', 'O').replace('ç', 'c').replace('Ç', 'C').replace('nan',''))
        # Reordering Columns
        new_order = ["Cliente/Fornecedor", "Número do Documento", "Valor (R$)", "Vencimento", "Quitado", "Data Realizado", "Observação", "Etiquetas"]
        df = df[new_order]
        df.to_csv("movimentacoes-filtradas.csv", index=False) # Save/Name File
        return df.head()
    except Exception as e:
            return e
        
def process_and_display(result_text, colunas_indesejadas):
    # Open Select File Window
    filepath = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    if filepath: # If Selected:
        result = process_file(filepath, colunas_indesejadas)
        if isinstance(result, str):  # If Result == Error Message
            return print_error(result_text, result)
        else:  
            return result_text.insert(tk.END, result)

def gui_setup():
    # Lista Colunas A Remover
    colunas_indesejadas = ['Conciliado', 'Quitado Parcialmente', 'Tipo', 'Transferência', 
    'Id da Conta Financeira', 'Nome da Conta Financeira', 
    'Tipo de Repetiçao', 'Parcela', 'Observação/Descrição', 
    'Competência', 'Data Conciliação', 'Valor Previsto', 
    'Valor Realizado', 'Valor Rateio', 'Valor Retenção', 
    'Quantidade de Parcelas', 'Origem da Renegociação', 
    'Boleto Gerado', 'Inicial', 'Categoria', 'Departamento', 
    'Tipo Cliente/Fornecedor', 'Documento Cliente/Fornecedor', 
    'Forma de Pagamento - Parcela', 'Forma de Pagamento - Quitação', 
    'Numero da Nota Fiscal', 'Nome Vendedor']
    root = tk.Tk() # Main Window:
    root.title("Filtrar Relatório Movimentação")

    result_text = tk.Text(root, height=5, width=50)
    result_text.pack()
    label = tk.Label(root,text="As colunas listadas abaixo serão removidas:", )
    label.pack(pady=10)
    label.config(font=("TkDefaultFont", 14), fg="black")
    label.config(state='disabled')

    text_frame = tk.Frame(root)
    text_frame.pack()
    text_scroll = tk.Scrollbar(text_frame, orient=tk.VERTICAL)
    text = tk.Text(text_frame, height='6', width='30', yscrollcommand=text_scroll.set)
    text_scroll.config(command=text.yview)
    text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    counter = len(colunas_indesejadas)
    for i in colunas_indesejadas:
        centered_text = i.center(text['width'])
        counter -=1
        if counter != 0:
            centered_text + '\n'
        text.insert(tk.END, centered_text)
        counter -= 1
    text.config(state='disabled')
    text.pack()

    process_button = tk.Button(root, text="Selecionar arquivo e processar", command=lambda: process_and_display(result_text, colunas_indesejadas))
    process_button.pack(pady=10,side='top', anchor='center')
    
    root.mainloop()

gui_setup()