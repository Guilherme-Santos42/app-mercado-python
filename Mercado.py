import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime

# Caminho para os relatórios
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
RELATORIO_FILE = os.path.join(DATA_DIR, "relatorio_produtos.xlsx")
RELATORIO_ATIVIDADES_FILE = os.path.join(DATA_DIR, "relatorio_atividades.xlsx")

# Dados iniciais
produtos = []
carrinho = []

# Função para carregar dados
def carregar_dados():
    global produtos
    if os.path.exists(RELATORIO_FILE):
        try:
            produtos.clear()
            df = pd.read_excel(RELATORIO_FILE)
            for _, row in df.iterrows():
                produtos.append({"Produto": row["Produto"], "Preço": row["Preço"], "Quantidade": int(row["Quantidade"])})
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")

# Função para salvar dados
def salvar_dados():
    df = pd.DataFrame(produtos)
    df.to_excel(RELATORIO_FILE, index=False)

# Função para registrar atividades
def registrar_atividade(atividade):
    try:
        df = pd.read_excel(RELATORIO_ATIVIDADES_FILE) if os.path.exists(RELATORIO_ATIVIDADES_FILE) else pd.DataFrame(columns=["Data/Hora", "Atividade"])
        nova_atividade = {"Data/Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Atividade": atividade}
        df = pd.concat([df, pd.DataFrame([nova_atividade])], ignore_index=True)
        df.to_excel(RELATORIO_ATIVIDADES_FILE, index=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao registrar atividade: {e}")

# Função para autenticação
def verificar_senha(menu_funcao):
    def verificar():
        senha = senha_entry.get()
        if senha == "1234":  # Altere a senha aqui
            popup.destroy()
            menu_funcao()
        else:
            messagebox.showerror("Erro", "Senha incorreta!")
            popup.destroy()

    popup = tk.Toplevel(root)
    popup.geometry("300x150")
    popup.title("Autenticação")
    tk.Label(popup, text="Digite a senha:", font=("Arial", 14)).pack(pady=10)
    senha_entry = ttk.Entry(popup, show="*", font=("Arial", 14))
    senha_entry.pack(pady=10)
    ttk.Button(popup, text="Entrar", command=verificar).pack(pady=10)

# Função para limpar a tela
def limpar_tela():
    for widget in root.winfo_children():
        widget.destroy()

# Função do menu principal
def menu_principal():
    limpar_tela()
    tk.Label(root, text="Sistema de Mercado", font=("Arial", 18, "bold")).pack(pady=20)

    ttk.Button(root, text="Cadastrar Produtos", command=lambda: verificar_senha(cadastrar_produtos)).pack(pady=10)
    ttk.Button(root, text="Produtos Cadastrados", command=lambda: verificar_senha(lista_produtos)).pack(pady=10)
    ttk.Button(root, text="Gerar Relatório", command=lambda: verificar_senha(gerar_relatorio)).pack(pady=10)
    ttk.Button(root, text="Mercado", command=mercado).pack(pady=10)

# Função para cadastrar produtos
def cadastrar_produtos():
    limpar_tela()
    tk.Label(root, text="Cadastrar Produtos", width=250, font=("Calibri", 10, "bold")).pack(pady=10)

    tk.Label(root, text="Nome do Produto:").pack()
    nome_entry = ttk.Entry(root)
    nome_entry.pack(pady=5)

    tk.Label(root, text="Preço:").pack()
    preco_entry = ttk.Entry(root)
    preco_entry.pack(pady=5)

    tk.Label(root, text="Quantidade:").pack()
    quantidade_entry = ttk.Entry(root)
    quantidade_entry.pack(pady=5)

    def salvar_produto():
        nome = nome_entry.get()
        preco = preco_entry.get()
        quantidade = quantidade_entry.get()
        if nome and preco and quantidade:
            try:
                produtos.append({"Produto": nome, "Preço": float(preco), "Quantidade": int(quantidade)})
                salvar_dados()
                registrar_atividade(f"Produto cadastrado: {nome} | Preço: R${float(preco):.2f} | Quantidade: {int(quantidade)}")
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                nome_entry.delete(0, tk.END)
                preco_entry.delete(0, tk.END)
                quantidade_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores válidos!")
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")

    ttk.Button(root, text="Salvar", command=salvar_produto).pack(pady=10)
    ttk.Button(root, text="Voltar", command=menu_principal).pack(pady=10)

# Função para listar produtos cadastrados
def lista_produtos():
    limpar_tela()
    tk.Label(root, text="Produtos Cadastrados", font=("Arial", 18, "bold")).pack(pady=10)

    for produto in produtos:
        texto = f'{produto["Produto"]} - R${produto["Preço"]:.2f} | Estoque: {produto["Quantidade"]}'
        tk.Label(root, text=texto).pack(pady=2)

    ttk.Button(root, text="Voltar", command=menu_principal).pack(pady=10)

# Função para gerar relatório
def gerar_relatorio():
    try:
        salvar_dados()
        registrar_atividade("Relatório de atividades gerado.")
        messagebox.showinfo("Sucesso", f"Relatórios gerados em: {DATA_DIR}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")

# Função do mercado
def mercado():
    limpar_tela()
    tk.Label(root, text="Mercado", font=("Arial", 18, "bold")).pack(pady=10)

    def adicionar_carrinho(produto):
        carrinho.append(produto)
        atualizar_total()

    def atualizar_total():
        total = sum(item["Preço"] for item in carrinho)
        total_label.config(text=f"Total: R${total:.2f}")

    def finalizar_venda():
        if not carrinho:
            messagebox.showinfo("Aviso", "O carrinho está vazio!")
            return

        detalhes_venda = []
        total_venda = 0

        for item in carrinho:
            for produto in produtos:
                if produto["Produto"] == item["Produto"]:
                    if produto["Quantidade"] > 0:
                        produto["Quantidade"] -= 1
                        total_venda += produto["Preço"]
                        detalhes_venda.append(f"{item['Produto']} (R${item['Preço']:.2f})")

        salvar_dados()
        detalhes = "; ".join(detalhes_venda)
        registrar_atividade(f"Venda realizada - Produtos: {detalhes} | Total: R${total_venda:.2f}")
        messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")
        menu_principal()

    for produto in produtos:
        ttk.Button(root, text=f"{produto['Produto']} - R${produto['Preço']:.2f}", command=lambda p=produto: adicionar_carrinho(p)).pack(pady=5)

    total_label = tk.Label(root, text="Total: R$0.00", font=("Arial", 14))
    total_label.pack(pady=10)

    ttk.Button(root, text="Finalizar Venda", command=finalizar_venda).pack(pady=10)
    ttk.Button(root, text="Voltar", command=menu_principal).pack(pady=10)

# Inicialização do programa
root = tk.Tk()
root.title("Sistema de Mercado")
root.geometry("600x600")
carregar_dados()
menu_principal()
root.mainloop()
