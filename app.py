import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as alert
from tkinter import *
import sqlite3

root = Tk()
root.title("Grade de matérias")
largura = 900
altura = 400
largura_screen = root.winfo_screenwidth()
altura_screen = root.winfo_screenheight()
x = (largura_screen/2) - (largura/2)
y = (altura_screen/2) - (altura/2)
root.geometry("%dx%d+%d+%d" % (largura, altura, x, y))
root.resizable(0, 0)
root.config(bg="#81F781")

updateJanela = None
id = None
janela = None

nome    = StringVar()
av      = StringVar()
av2     = StringVar()
av3     = StringVar()
avd     = StringVar()
avds    = StringVar()

def isNumero(value):
    try:
        float(value)
    except ValueError:
        return False
    return True

def limpaCampos():
    nome.set("")
    av.set("")
    av2.set("")
    av3.set("")
    avd.set("")
    avds.set("")

def gerarTabela(fetch):
    for data in fetch:
        tree.insert('', 'end', values=(data))

def criarTabela():
    conn = sqlite3.connect("materias.db")
    cursor = conn.cursor()
    query = """ CREATE TABLE IF NOT EXISTS 'materias' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT, av REAL, av2 REAL, av3 REAL, avd REAL, avds REAL, media REAL, situacao TEXT) """
    cursor.execute(query)
    cursor.execute('SELECT * FROM materias ORDER BY nome')
    fetch = cursor.fetchall()
    gerarTabela(fetch)
    cursor.close()
    conn.close()


def inserirMateria():
    if nome.get() == '' or isNumero(nome.get()) or (av.get() != '' and not isNumero(av.get())) or (av2.get() != '' and not isNumero(av2.get())) or (av3.get() != '' and not isNumero(av3.get())) or (avd.get() != '' and not isNumero(avd.get())) or (avds.get() != '' and not isNumero(avds.get())):
        alert.showwarning("", "Campos de notas devem ser de valor numérico e o nome da matéria deve ser preenchido e não pode ser um número", icon="warning")
        return

    tree.delete(*tree.get_children())

    if av.get() == '' or av2.get() == '' or avd.get() == '':
        media = 0
        situacao = ''
    else:
        nota1 = float(av.get())
        nota2 = float(av2.get())
        nota3 = float(avd.get())

        if av3.get() != '':
            temp = float(av3.get())
            if nota1 < nota2:
                if temp > nota1: 
                    nota1 = temp
            else:
                if temp > nota2: 
                    nota2 = temp
        
        if avds.get() != '':
            temp = float(avds.get())
            if temp > nota3: 
                nota3 = temp

        media = round((nota1+nota2+nota3)/3, 1)
        if media >= 6.0:
            situacao = 'Aprovado'
        else:
            situacao = 'Reprovado'

    conn = sqlite3.connect("materias.db")
    cursor = conn.cursor()
    query = """ INSERT INTO 'materias' (nome, av, av2, av3, avd, avds, media, situacao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (str(nome.get()), str(av.get()), str(av2.get()), str(av3.get()), str(avd.get()), str(avds.get()), media, situacao))
    conn.commit()
    cursor.execute('SELECT * FROM materias ORDER BY nome')
    fetch = cursor.fetchall()
    gerarTabela(fetch)
    cursor.close()
    conn.close()
    limpaCampos()

def lancarNota():
    if (av.get() != '' and not isNumero(av.get())) or (av2.get() != '' and not isNumero(av2.get())) or (av3.get() != '' and not isNumero(av3.get())) or (avd.get() != '' and not isNumero(avd.get())) or (avds.get() != '' and not isNumero(avds.get())):
        alert.showwarning("", "Campos de notas devem ser de valor numérico", icon="warning")
        return

    tree.delete(*tree.get_children())

    if av.get() == '' or av2.get() == '' or avd.get() == '':
        media = 0
        situacao = ''
    else:
        nota1 = float(av.get())
        nota2 = float(av2.get())
        nota3 = float(avd.get())

        if av3.get() != '':
            temp = float(av3.get())
            if nota1 < nota2:
                if temp > nota1: 
                    nota1 = temp
            else:
                if temp > nota2: 
                    nota2 = temp
        
        if avds.get() != '':
            temp = float(avds.get())
            if temp > nota3: 
                nota3 = temp

        media = round((nota1+nota2+nota3)/3, 1)
        if media >= 6.0:
            situacao = 'Aprovado'
        else:
            situacao = 'Reprovado'

    conn = sqlite3.connect("materias.db")
    cursor = conn.cursor()
    query = """ UPDATE 'materias' SET nome = ?, av = ?, av2 = ?, av3 = ?, avd = ?, avds = ?, media = ?, situacao = ? WHERE id = ?"""
    cursor.execute(query, (str(nome.get()), str(av.get()),
                           str(av2.get()), str(av3.get()), str(avd.get()), str(avds.get()), media, situacao, int(id)))
    conn.commit()
    cursor.execute('SELECT * FROM materias ORDER BY nome')
    fetch = cursor.fetchall()
    gerarTabela(fetch)
    cursor.close()
    conn.close()
    limpaCampos()
    updateJanela.destroy()

def selecionarCampo(event):
    global id, updateJanela
    lista_itens = tree.focus()
    conteudo = (tree.item(lista_itens))
    itens = conteudo["values"]
    id = itens[0]
    limpaCampos()
    nome.set(itens[1])
    av.set(itens[2])
    av2.set(itens[3])
    av3.set(itens[4])
    avd.set(itens[5])
    avds.set(itens[6])

    updateJanela = Toplevel()
    updateJanela.title("LANÇAMENTO DE NOTAS")
    largura = 550
    altura = 300
    largura_screen = updateJanela.winfo_screenwidth()
    altura_screen = updateJanela.winfo_screenheight()
    x = (largura_screen/2) - (largura/2)
    y = (altura_screen/2) - (altura/2)
    updateJanela.geometry("%dx%d+%d+%d" % (largura, altura, x, y))
    updateJanela.resizable(0, 0)

    form_title = Frame(updateJanela)
    form_title.pack(side=TOP)
    form_materias = Frame(updateJanela)
    form_materias.pack(side = TOP, pady = 10)

    lbl_title = Label(form_title, text="Atualize as notas da matéria selecionada aqui:", font=('arial', 18), bg='blue', fg='white', width=300)
    lbl_title.pack(fill=X)
    lbl_materia = Label(form_title, textvariable=nome, font='arial 25 bold', bg='blue', fg='white', width=300, pady=5)
    lbl_materia.pack(fill=X)

    lbl_av = Label(form_materias, text="AV", font=('arial', 12))
    lbl_av.grid(row=0, sticky=W)
    lbl_av2 = Label(form_materias, text="AV2", font=('arial', 12))
    lbl_av2.grid(row=1, sticky=W)
    lbl_av3 = Label(form_materias, text="AV3", font=('arial', 12))
    lbl_av3.grid(row=2, sticky=W)
    lbl_avd = Label(form_materias, text="AVD", font=('arial', 12))
    lbl_avd.grid(row=3, sticky=W)
    lbl_avds = Label(form_materias, text="AVDS", font=('arial', 12))
    lbl_avds.grid(row=4, sticky=W)

    av_entry = Entry(form_materias, textvariable=av, font=('arial', 12))
    av_entry.grid(row=0, column=1)
    av2_entry = Entry(form_materias, textvariable=av2, font=('arial', 12))
    av2_entry.grid(row=1, column=1)
    av3_entry = Entry(form_materias, textvariable=av3, font=('arial', 12))
    av3_entry.grid(row=2, column=1)
    avd_entry = Entry(form_materias, textvariable=avd, font=('arial', 12))
    avd_entry.grid(row=3, column=1)
    avds_entry = Entry(form_materias, textvariable=avds, font=('arial', 12))
    avds_entry.grid(row=4, column=1)
    
    btn_update = Button(form_materias, text="Atualizar", width=50, command=lancarNota)
    btn_update.grid(row=6, columnspan=2, pady=10)

def apagarMateria():
    if not tree.selection():
        resultado = alert.showwarning("", "Por favor, selecione uma matéria da lista para realizar o comendo.", icon="warning")
    else:
        lista_itens = tree.focus()
        conteudo = (tree.item(lista_itens))
        itens = conteudo['values']
        nome = itens[1]
        resultado = alert.askquestion("", f"Tem certeza que deseja apagar a matéria {nome} da grade de Luciano?")
        if resultado == 'yes':

            tree.delete(lista_itens)
            conn = sqlite3.connect("materias.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM 'materias' WHERE id = %d" % itens[0])
            conn.commit()
            cursor.close()
            conn.close()

def novaMateria():
    global janela
    limpaCampos()


    janela = Toplevel()
    janela.title("NOVA MATÉRIA")
    largura = 480
    altura = 300
    largura_screen = janela.winfo_screenwidth()
    altura_screen = janela.winfo_screenheight()
    x = (largura_screen/2) - (largura/2)
    y = (altura_screen/2) - (altura/2)
    janela.geometry("%dx%d+%d+%d" % (largura, altura, x, y))
    janela.resizable(0, 0)

    
    form_title = Frame(janela)
    form_title.pack(side=TOP)
    form_materias = Frame(janela)
    form_materias.pack(side=TOP, pady=10)
    
    lbl_title = Label(form_title, text="Preencha os campos para adicionar matéria",
                      font=('arial', 18), bg='blue',fg='white' , width=300, pady=5)
    lbl_title.pack(fill=X)
    lbl_nome = Label(form_materias, text="Nome", font=('arial', 12))
    lbl_nome.grid(row=0, sticky=W)
    lbl_av = Label(form_materias, text="AV", font=('arial', 12))
    lbl_av.grid(row=1, sticky=W)
    lbl_av2 = Label(form_materias, text="AV2", font=('arial', 12))
    lbl_av2.grid(row=2, sticky=W)
    lbl_av3 = Label(form_materias, text="AV3", font=('arial', 12))
    lbl_av3.grid(row=3, sticky=W)
    lbl_avd = Label(form_materias, text="AVD", font=('arial', 12))
    lbl_avd.grid(row=4, sticky=W)
    lbl_avds = Label(form_materias, text="AVDS", font=('arial', 12))
    lbl_avds.grid(row=5, sticky=W)

    
    nome_entry = Entry(form_materias, textvariable=nome, font=('arial', 12))
    nome_entry.grid(row=0, column=1)
    av_entry = Entry(form_materias, textvariable=av, font=('arial', 12))
    av_entry.grid(row=1, column=1)
    av2_entry = Entry(form_materias, textvariable=av2, font=('arial', 12))
    av2_entry.grid(row=2, column=1)
    av3_entry = Entry(form_materias, textvariable=av3, font=('arial', 12))
    av3_entry.grid(row=3, column=1)
    avd_entry = Entry(form_materias, textvariable=avd, font=('arial', 12))
    avd_entry.grid(row=4, column=1)
    avds_entry = Entry(form_materias, textvariable=avds, font=('arial', 12))
    avds_entry.grid(row=5, column=1)

    btn_inserir = Button(form_materias, text="Inserir",
                        width=50, command=inserirMateria)
    btn_inserir.grid(row=6, columnspan=2, pady=10)


top = Frame(root, width=800, bd=1, relief=SOLID)
top.pack(side=TOP)
lateral = Frame(root, width=100, height=300, bg="#81F781")
lateral.pack(side=LEFT)

lateralTop = Frame(lateral, width=100)
lateralTop.pack(side=TOP, pady=10)

lateralAviso = Frame(lateral, width=100)
lateralAviso.pack(side=BOTTOM, pady=85, padx=20)

lateralBottom = Frame(lateral, width=100)
lateralBottom.pack(side=BOTTOM, pady=10)

tabelaMaterias = Frame(root, width=500)
tabelaMaterias.pack(side=RIGHT, pady=20, padx=20)


lbl_title = Label(top, text="Grade de matérias de Luciano", font='arial 18 bold italic', width=500) 
lbl_title.pack(fill=X)

lbl_aviso = Label(lateralAviso, text="Para atualizar o lançamento\n das notas, clique duas vezes\n na matéria desejada.", font='arial 16 bold')
lbl_aviso.pack(fill=X)


btn_add = Button(lateralTop, text="Nova matéria", width=20, height=2, command=novaMateria)
btn_add.pack(side=TOP)
btn_del = Button(lateralBottom, text="Deletar matéria", width=20, height=2, command=apagarMateria)
btn_del.pack()

scrollbarX = Scrollbar(tabelaMaterias, orient=HORIZONTAL)
scrollbarY = Scrollbar(tabelaMaterias, orient=VERTICAL)

tree = ttk.Treeview(tabelaMaterias, columns=("id", "Nome", "AV", "AV2", "AV3", "AVD", "AVDS", "Média", "Situação"), height=400, selectmode="extended", yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
scrollbarY.config(command=tree.yview)
scrollbarY.pack(side=RIGHT, fill=Y)
scrollbarX.config(command=tree.xview)
scrollbarX.pack(side=BOTTOM, fill=X)
tree.heading("id", text="id", anchor=W)
tree.heading("Nome", text="Nome", anchor=W)
tree.heading("AV", text="AV", anchor=W)
tree.heading("AV2", text="AV2", anchor=W)
tree.heading("AV3", text="AV3", anchor=W)
tree.heading("AVD", text="AVD", anchor=W)
tree.heading("AVDS", text="AVDS", anchor=W)
tree.heading("Média", text="Média", anchor=W)
tree.heading("Situação", text="Situação", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=1)
tree.column('#1', stretch=NO, minwidth=0, width=40)
tree.column('#2', stretch=NO, minwidth=0, width=150)
tree.column('#3', stretch=NO, minwidth=0, width=50)
tree.column('#4', stretch=NO, minwidth=0, width=50)
tree.column('#5', stretch=NO, minwidth=0, width=50)
tree.column('#6', stretch=NO, minwidth=0, width=50)
tree.column('#7', stretch=NO, minwidth=0, width=50)
tree.column('#8', stretch=NO, minwidth=0, width=50)
tree.column('#9', stretch=NO, minwidth=0, width=80)
tree.pack()
tree.bind('<Double-Button-1>', selecionarCampo)

barra_superior = Menu(root)
root.config(menu=barra_superior)

meu_menu = Menu(barra_superior, tearoff = 0)
barra_superior.add_cascade(label="Menu", menu=meu_menu)
meu_menu.add_command(label="Adicionar nova matéria", command=novaMateria)
meu_menu.add_separator()
meu_menu.add_command(label="Sair", command=root.destroy)




if __name__ == '__main__':
    criarTabela()
    root.mainloop()
