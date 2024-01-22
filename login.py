import warnings
import customtkinter as custom
from tkinter import *
import mysql.connector

def center(win):
    # :param win: the main window or Toplevel window to center

    # Apparently a common hack to get the window size. Temporarily hide the
    # window to avoid update_idletasks() drawing the window in the wrong
    # position.
    win.update_idletasks()  # Update "requested size" from geometry manager

    # define window dimensions width and height
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width

    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width

    # Get the window position from the top dynamically as well as position from left or right as follows
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2

    # this is the line that will center your window
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    # This seems to draw the window frame immediately, so only call deiconify()
    # after setting correct window position
    win.deiconify()

def view(usuario):
    comando = f""" SELECT * FROM logins
    WHERE usuario = '{usuario}'
"""
    cursor.execute(comando)
    resultado = cursor.fetchall()
    print(resultado)

# Configuracoes da base de dados
# table name: logins
# columns: id, usuario, senha, checkbox

# FUNCOES BANCO DE DADOS
def get_checkbox(usuario):
    comando = f""" SELECT * FROM logins
    WHERE usuario = '{usuario}'
"""
    cursor.execute(comando)
    lista_usuario = cursor.fetchall()
    return lista_usuario[0][3]

def get_login(usuario):
    comando = f"""SELECT * FROM logins
    where usuario = '{usuario}'
    """
    cursor.execute(comando)
    resultado = cursor.fetchall()
    login = resultado[0][1].lower()
    senha = resultado[0][2]
    checkbox = resultado[0][3] # FALTA ARRUMAR
    return login, senha

def alterar_checkbox(usuario, valor):
    comando = f""" UPDATE logins
    SET checkbox = {valor}
    WHERE usuario = '{usuario}'
    """
    cursor.execute(comando)
    conexao.commit()



conexao = mysql.connector.connect(
    host='localhost', # Seu host
    user='root', # Seu usuario
    password='123456', # Sua senha
    database='cabal' # Nome do seu banco de dados
)
print("Conexão bem sucedida!")
cursor = conexao.cursor()

f = ("Roboto", 15)

custom.set_appearance_mode("Dark")
janela = custom.CTk()
janela.geometry("700x300")
janela.title("Login")
janela.resizable(False, False)
center(janela)

# INICIO FILTRO DE AVISO
warnings.filterwarnings("ignore")
# Background
img = PhotoImage(file=r"C:\Users\hugom\Desktop\Programacao\Sistema_de_login\newton.png") # Local da imagem. 
# Dimensionamento da imagem
img = img.zoom(35, 25) 
img = img.subsample(70, 40)
################################
label_img = custom.CTkLabel(janela, image=img, text="")
label_img.place(x=0, y=0)
# FIM FILTRO DE AVISO
warnings.filterwarnings("always")

# frame
frame = custom.CTkFrame(janela, width=350, height=300)
frame.pack(side=RIGHT)

# Sistema
text = custom.CTkLabel(frame, text="Morgan\'s Academy", font=("Roboto", 30))
text.place(x=50, y=20)

# id
login1 = custom.CTkLabel(frame, text="Login:", font=f)
login1.place(x=50, y=75)
login2 = custom.CTkEntry(frame, width=170, placeholder_text="Insira aqui seu usuário", font=f)
# login_text = custom.StringVar()
# login2 = custom.CTkEntry(frame, width=170, textvariable=login_text, font=f) # TENTATIVA DE UTILIZAR A CHECKBOX
login2.place(x=100, y=75)
login = login2.get()

# senha
senha1 = custom.CTkLabel(frame, text="Senha:", font=f)
senha1.place(x=50, y=130)
senha2 = custom.CTkEntry(frame, width=170, placeholder_text="Insira aqui sua senha" , font=f, show="*")
senha2.place(x=100, y=130)
senha = senha2.get()

# Checkbox -> 0 = desativado; 1 = ativado.
def trocar():
    login = login2.get()
    valor = check.get()
    alterar_checkbox(login, valor)

v = custom.IntVar()
check = custom.CTkCheckBox(frame, text="Lembrar login", variable=v)
check.place(x=53, y=173)

def entrar():
    # Dados fornecidos
    login = login2.get().lower()
    senha = senha2.get()
    checkbox = check.get()
    print(f"login: {login} Senha: {senha} Checkbox: {checkbox}")
    # Condicao de login
    condicao = custom.StringVar()
    erro = custom.CTkLabel(master=frame, height=10, width=170, textvariable=condicao, text_color="red", font=("Roboto", 12))
    erro.place(x=30, y=205)
    try:
        login, senha_correta = get_login(login)
        if senha == "":
            condicao.set("insira sua senha.")
        elif senha != senha_correta:
            condicao.set("Senha incorreta.")
            senha2.delete(0, END)
            # senha2.insert(0, "")
        elif senha == senha_correta:
            trocar()
            view(login)
            # janela.after(150, janela.destroy())
            print("EXECUTA ACAO") ########################### -> Altere aqui o resultado
    except:
        condicao.set("Usuario não existe.")
        senha2.delete(0, END)

# entrar       
enter = custom.CTkButton(frame, text="Entrar", command=entrar)
enter.place(x=100, y=240)


janela.mainloop()
cursor.close()
conexao.close()