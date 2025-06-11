import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import hashlib
import re
from medalhas import OlympicMedalsViewer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DB_NOME = "usuarios.db"

def criar_tabelas(): # usuarios e senhas
    conn = sqlite3.connect(DB_NOME)
    c = conn.cursor()

    # Tabela de usuários
    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)

    # Tabela de senhas
    c.execute("""
        CREATE TABLE IF NOT EXISTS senhas (
            user_id INTEGER PRIMARY KEY,
            senha_hash TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES usuarios (id)
        )
    """)
    conn.commit()
    conn.close()

def hash_senha(senha): # codificador de senha
    return hashlib.sha256(senha.encode()).hexdigest()

def validar_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def validar_telefone(telefone):
    return re.match(r'^[1-9]{2}[0-9]{8,9}$', telefone)

def validar_forca_senha(senha): # validaçao de letra maiuscula e minuscula e caractere
    return (
        re.search(r'[A-Z]', senha) and
        re.search(r'[a-z]', senha) and
        re.search(r'[^a-zA-Z0-9]', senha)
    )

class LoginCadastroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login / Cadastro")
        self.root.geometry("400x640")
        criar_tabelas()
        self.criar_tela_login()

    def criar_tela_login(self): # cria a tela de login e os cmpos de entrada
        self.limpar_tela()
        self.frame = ctk.CTkFrame(self.root, fg_color="#0d1117", corner_radius=15)
        self.frame.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="🏅 Bem-vindo!", font=ctk.CTkFont(size=24, weight="bold"), text_color="#3b82f6").pack(pady=(30, 10))

        self.username = ctk.CTkEntry(self.frame, placeholder_text="Usuário ou telefone", width=300)
        self.username.pack(pady=15)

        self.senha = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*", width=300)
        self.senha.pack(pady=5)

        self.mostrar_senha_login = False
        self.toggle_btn = ctk.CTkButton(self.frame, text="👁 Mostrar", width=80, command=self.toggle_senha_login)
        self.toggle_btn.pack(pady=(0, 15))

        ctk.CTkButton(self.frame, text="🔐 Login", command=self.fazer_login, width=200, height=40, fg_color="#3b82f6").pack(pady=(10, 10))
        ctk.CTkButton(self.frame, text="📝 Cadastrar", command=self.criar_tela_cadastro, width=200, height=40, fg_color="#3b82f6").pack()
        ctk.CTkButton(self.frame, text="🔑 Esqueci minha senha", command=self.abrir_tela_redefinir, width=100, height=25, fg_color="#19458a").pack(pady=(10, 10)) ###################

    def criar_tela_cadastro(self): # cria a tela de cadastro para novos usuarios
        self.limpar_tela()
        self.frame = ctk.CTkFrame(self.root, fg_color="#0d1117", corner_radius=15)
        self.frame.pack(pady=20, padx=40, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="📝 Cadastro", font=ctk.CTkFont(size=22, weight="bold"), text_color="#3b82f6").pack(pady=(20, 10))

        self.entry_usuario = ctk.CTkEntry(self.frame, placeholder_text="Nome de usuário", width=300)
        self.entry_usuario.pack(pady=5)

        self.entry_email = ctk.CTkEntry(self.frame, placeholder_text="Email", width=300)
        self.entry_email.pack(pady=5)

        self.entry_telefone = ctk.CTkEntry(self.frame, placeholder_text="Telefone com DDD (ex: 81999999999)", width=300)
        self.entry_telefone.pack(pady=5)

        self.entry_senha = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*", width=300)
        self.entry_senha.pack(pady=5)

        self.entry_confirmar = ctk.CTkEntry(self.frame, placeholder_text="Confirmar senha", show="*", width=300)
        self.entry_confirmar.pack(pady=5)

        self.mostrar_senha_cadastro = False
        self.toggle_cadastro_btn = ctk.CTkButton(self.frame, text="👁 Mostrar", width=80, command=self.toggle_senha_cadastro)
        self.toggle_cadastro_btn.pack(pady=(0, 10))

        ctk.CTkButton(self.frame, text="✔ Cadastrar", command=self.fazer_cadastro, width=200).pack(pady=(10, 10))
        ctk.CTkButton(self.frame, text="⬅ Voltar", command=self.criar_tela_login, width=200, fg_color="#64748b").pack()

    def fazer_cadastro(self): # registra um novo usuario no banco de dados
        usuario = self.entry_usuario.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        senha = self.entry_senha.get()
        confirmar = self.entry_confirmar.get()

        if not all([usuario, email, telefone, senha, confirmar]):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
        if not validar_forca_senha(senha):
            messagebox.showerror("Erro", "A senha deve conter pelo menos:\n- Uma letra maiúscula\n- Uma letra minúscula\n- Um caractere especial.")
            return
        if not validar_email(email):
            messagebox.showerror("Erro", "Email inválido.")
            return
        if not validar_telefone(telefone):
            messagebox.showerror("Erro", "Telefone inválido. Ex: +5581999999999")
            return

        conn = sqlite3.connect(DB_NOME)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO usuarios (username, telefone, email) VALUES (?, ?, ?)", (usuario, telefone, email))
            user_id = c.lastrowid
            c.execute("INSERT INTO senhas (user_id, senha_hash) VALUES (?, ?)", (user_id, hash_senha(senha)))
            conn.commit()
            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
            self.criar_tela_login()
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                messagebox.showerror("Erro", "Este nome de usuário já existe.")
            elif "email" in str(e):
                messagebox.showerror("Erro", "Este email já está cadastrado.")
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar.")
        finally:
            conn.close()

    def fazer_login(self): # faz a validaçao do usuario atraves de username ou numero de celular
        usuario = self.username.get().strip()
        senha = self.senha.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        conn = sqlite3.connect(DB_NOME)
        c = conn.cursor()
        c.execute("SELECT id, username FROM usuarios WHERE username = ? OR telefone = ?", (usuario, usuario))
        resultado = c.fetchone()

        if resultado:
            user_id, nome = resultado
            c.execute("SELECT senha_hash FROM senhas WHERE user_id = ?", (user_id,))
            senha_hash_db = c.fetchone()
            conn.close()

            if senha_hash_db and hash_senha(senha) == senha_hash_db[0]:
                self.muda_para_medalhas_py(nome)
                return

        conn.close()
        resposta = messagebox.askquestion("Login falhou", "Usuário ou senha incorretos.\nDeseja se cadastrar?")
        if resposta == "yes":
            self.criar_tela_cadastro()

    def abrir_tela_redefinir(self): # interface para redefinir senha
        self.limpar_tela()
        self.frame = ctk.CTkFrame(self.root, fg_color="#0d1117", corner_radius=15)
        self.frame.pack(pady=30, padx=40, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="🔐 Redefinir Senha", font=ctk.CTkFont(size=22, weight="bold"), text_color="#3b82f6").pack(pady=20)

        self.recuperacao = ctk.CTkEntry(self.frame, placeholder_text="Digite seu email ou telefone", width=300)
        self.recuperacao.pack(pady=10)

        self.nova_senha = ctk.CTkEntry(self.frame, placeholder_text="Nova senha", show="*", width=300)
        self.nova_senha.pack(pady=10)

        self.confirma_nova = ctk.CTkEntry(self.frame, placeholder_text="Confirmar nova senha", show="*", width=300)
        self.confirma_nova.pack(pady=10)

        self.toggle_reset_btn = ctk.CTkButton(self.frame, text="👁 Mostrar", width=80, command=self.toggle_reset_senha)
        self.toggle_reset_btn.pack(pady=(0, 10))

        self.mostrar_reset = False

        ctk.CTkButton(self.frame, text="✔ Atualizar senha", command=self.redefinir_senha, width=200).pack(pady=(10, 10))
        ctk.CTkButton(self.frame, text="⬅ Voltar", command=self.criar_tela_login, width=200, fg_color="#64748b").pack()

    def redefinir_senha(self): # atualiza a senha apos a validaçao
        identificador = self.recuperacao.get().strip()
        nova = self.nova_senha.get()
        confirma = self.confirma_nova.get()

        if not all([identificador, nova, confirma]):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        if nova != confirma:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
        if not validar_forca_senha(nova):
            messagebox.showerror("Erro", "A senha deve conter pelo menos:\n- Uma letra maiúscula\n- Uma letra minúscula\n- Um caractere especial.")
            return

        conn = sqlite3.connect(DB_NOME)
        c = conn.cursor()
        c.execute("SELECT id FROM usuarios WHERE email = ? OR telefone = ?", (identificador, identificador))
        usuario = c.fetchone()

        if not usuario:
            messagebox.showerror("Erro", "Email ou telefone não encontrado.")
            conn.close()
            return

        user_id = usuario[0]
        c.execute("UPDATE senhas SET senha_hash = ? WHERE user_id = ?", (hash_senha(nova), user_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Senha atualizada com sucesso!")
        self.criar_tela_login()

    def toggle_senha_login(self): # alterna entre mostrar e ocultar a senha na tela de login
        self.mostrar_senha_login = not self.mostrar_senha_login
        self.senha.configure(show="" if self.mostrar_senha_login else "*")
        self.toggle_btn.configure(text="🙈 Ocultar" if self.mostrar_senha_login else "👁 Mostrar")

    def toggle_reset_senha(self): # alterna entre mostrar e ocultar a senha na tela de redefiniçao
        self.mostrar_reset = not self.mostrar_reset
        mostrar = "" if self.mostrar_reset else "*"
        self.nova_senha.configure(show=mostrar)
        self.confirma_nova.configure(show=mostrar)
        self.toggle_reset_btn.configure(text="🙈 Ocultar" if self.mostrar_reset else "👁 Mostrar")   #

    def toggle_senha_cadastro(self): # alterna entre mostrar e ocultar a senha na tela de cadastro
        self.mostrar_senha_cadastro = not self.mostrar_senha_cadastro
        show_char = "" if self.mostrar_senha_cadastro else "*"
        self.entry_senha.configure(show=show_char)
        self.entry_confirmar.configure(show=show_char)
        self.toggle_cadastro_btn.configure(text="🙈 Ocultar" if self.mostrar_senha_cadastro else "👁 Mostrar")

    def limpar_tela(self): # remove os widget da janela
        for widget in self.root.winfo_children():
            widget.destroy()

    def muda_para_medalhas_py(self, nome_usuario): # muda para a interfce de pesquisa apos a validaçao do usuario
        self.limpar_tela()
        OlympicMedalsViewer(self.root) 

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginCadastroApp(root)
    root.mainloop()