import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msb
from tkinter import *
import sqlite3

root = Tk()
root.title("Lista de contatos")
width = 800
height = 400
sc_width = root.winfo_screenwidth()
sc_height = root.winfo_screenheight()
x = (sc_width/2) - (width/2)
y = (sc_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
# root.iconbitmap("Nova America/Noite/icons/crud.ico")
root.config(bg="#81F781")

# --------- VARIAVEIS ----------

nome    = StringVar()
av      = StringVar()
av2     = StringVar()
av3     = StringVar()
avd     = StringVar()
avds     = StringVar()
updateWindow = None
id = None
newWindow = None

# ------------ METODOS ----------

def limpa_campos():
    nome.set("")
    av.set("")
    av2.set("")
    av3.set("")
    avd.set("")
    avds.set("")


def database():
    conn = sqlite3.connect("materias.db")
    cursor = conn.cursor()
    query = """ CREATE TABLE IF NOT EXISTS 'materias' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT, av INTEGER, av2 INTEGER, av3 INTEGER, avd INTEGER, avds INTEGER) """
    cursor.execute(query)
    cursor.execute('SELECT * FROM materias ORDER BY nome')
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


def submitData():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect("materias.db")
    cursor = conn.cursor()
    query = """ INSERT INTO 'materias' (nome, av, av2, av3, avd, avds) VALUES (?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (str(nome.get()), str(av.get()), str(av2.get()), str(av3.get()), str(avd.get()), str(avds.get())))
    conn.commit()
    cursor.execute('SELECT * FROM materias ORDER BY nome')
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    limpa_campos()

def updateData():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect("materias.db")
    cursor = conn.cursor()
    query = """ UPDATE 'materias' SET nome = ?, av = ?, av2 = ?, av3 = ?, avd = ?, avds = ? WHERE id = ?"""
    cursor.execute(query, (str(nome.get()), str(av.get()),
                           str(av2.get()), str(av3.get()), str(avd.get()), str(avds.get()), int(id)))
    conn.commit()
    cursor.execute('SELECT * FROM materias ORDER BY nome')
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    limpa_campos()
    updateWindow.destroy()

def onSelect(event):
    global id, updateWindow
    selectItem = tree.focus()
    conteudo = (tree.item(selectItem))
    selectedItem = conteudo["values"]
    id = selectedItem[0]
    limpa_campos()
    nome.set(selectedItem[1])
    av.set(selectedItem[2])
    av2.set(selectedItem[3])
    av3.set(selectedItem[4])
    avd.set(selectedItem[5])
    avds.set(selectedItem[6])

    #--------- CRIANDO JANELA UPDATE ---------
    updateWindow = Toplevel()
    updateWindow.title("ATUALIZANDO CONTATO")
    width = 480
    heigth = 200
    sc_width = updateWindow.winfo_screenwidth()
    sc_height = updateWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    updateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    updateWindow.resizable(0, 0)

    # --------- FRAME DO ATUALIZAR ----------
    formTitle = Frame(updateWindow)
    formTitle.pack(side=TOP)
    formContact = Frame(updateWindow)
    formContact.pack(side = TOP, pady = 10)
    # --------- LABEL DO ATUALIZAR ----------
    lbl_title = Label(formTitle, text="Atualizando contato", font=('arial', 18), bg='blue', width=300)
    lbl_title.pack(fill=X)
    lbl_nome = Label(formContact, text="Nome", font=('arial', 12))
    lbl_nome.grid(row=0, sticky=W)
    lbl_av = Label(formContact, text="av", font=('arial', 12))
    lbl_av.grid(row=1, sticky=W)
    lbl_av2 = Label(formContact, text="av2", font=('arial', 12))
    lbl_av2.grid(row=2, sticky=W)
    lbl_av3 = Label(formContact, text="av3", font=('arial', 12))
    lbl_av3.grid(row=3, sticky=W)
    lbl_avd = Label(formContact, text="avd", font=('arial', 12))
    lbl_avd.grid(row=4, sticky=W)
    lbl_avds = Label(formContact, text="avds", font=('arial', 12))
    lbl_avds.grid(row=5, sticky=W)

    # --------- ENTRY DO ATUALIZAR ----------
    nome_Entry = Entry(formContact, textvariable=nome, font=('arial', 12))
    nome_Entry.grid(row=0, column=1)
    av_Entry = Entry(formContact, textvariable=av, font=('arial', 12))
    av_Entry.grid(row=1, column=1)
    av2_Entry = Entry(formContact, textvariable=av2, font=('arial', 12))
    av2_Entry.grid(row=2, column=1)
    av3_Entry = Entry(formContact, textvariable=av3, font=('arial', 12))
    av3_Entry.grid(row=3, column=1)
    avd_Entry = Entry(formContact, textvariable=avd, font=('arial', 12))
    avd_Entry.grid(row=4, column=1)
    avds_Entry = Entry(formContact, textvariable=avds, font=('arial', 12))
    avds_Entry.grid(row=5, column=1)
    
    # --------- BUTTON DO ATUALIZAR ---------
    bttn_update = Button(formContact, text="Atualizar", width=50, command=updateData)
    bttn_update.grid(row=6, columnspan=2, pady=10)

def deletarData():
    if not tree.selection():
        resultado = msb.showwarning("", "Por favor, selecione um item na lista.", icon="warning")
    else:
        resultado = msb.askquestion("", "Tem certeza que deseja deletar o contato?")
        if resultado == 'yes':
            selectItem = tree.focus()
            conteudo = (tree.item(selectItem))
            selectedItem = conteudo['values']
            tree.delete(selectItem)
            conn = sqlite3.connect("materias.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM 'materias' WHERE id = %d" % selectedItem[0])
            conn.commit()
            cursor.close()
            conn.close()

def inserirData():
    global newWindow
    limpa_campos()

    #--------- CRIANDO JANELA INCLUDE ---------
    newWindow = Toplevel()
    newWindow.title("INSERINDO MATÉRIA")
    width = 480
    heigth = 200
    sc_width = newWindow.winfo_screenwidth()
    sc_height = newWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    newWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    newWindow.resizable(0, 0)

    # --------- FRAME DO INCLUDE ----------
    formTitle = Frame(newWindow)
    formTitle.pack(side=TOP)
    formContact = Frame(newWindow)
    formContact.pack(side=TOP, pady=10)
    # --------- LABEL DO INCLUDE ----------
    lbl_title = Label(formTitle, text="Inserindo contato",
                      font=('arial', 18), bg='blue', width=300)
    lbl_title.pack(fill=X)
    lbl_nome = Label(formContact, text="nome", font=('arial', 12))
    lbl_nome.grid(row=0, sticky=W)
    lbl_av = Label(formContact, text="av", font=('arial', 12))
    lbl_av.grid(row=1, sticky=W)
    lbl_av2 = Label(formContact, text="av2", font=('arial', 12))
    lbl_av2.grid(row=2, sticky=W)
    lbl_av3 = Label(formContact, text="av3", font=('arial', 12))
    lbl_av3.grid(row=3, sticky=W)
    lbl_avd = Label(formContact, text="avd", font=('arial', 12))
    lbl_avd.grid(row=4, sticky=W)
    lbl_avds = Label(formContact, text="avds", font=('arial', 12))
    lbl_avds.grid(row=5, sticky=W)

    # --------- ENTRY DO INCLUDE ----------
    nome_Entry = Entry(formContact, textvariable=nome, font=('arial', 12))
    nome_Entry.grid(row=0, column=1)
    av_Entry = Entry(formContact, textvariable=av, font=('arial', 12))
    av_Entry.grid(row=1, column=1)
    av2_Entry = Entry(formContact, textvariable=av2, font=('arial', 12))
    av2_Entry.grid(row=2, column=1)
    av3_Entry = Entry(formContact, textvariable=av3, font=('arial', 12))
    av3_Entry.grid(row=3, column=1)
    avd_Entry = Entry(formContact, textvariable=avd, font=('arial', 12))
    avd_Entry.grid(row=4, column=1)
    avds_Entry = Entry(formContact, textvariable=avds, font=('arial', 12))
    avds_Entry.grid(row=5, column=1)

    # --------- BUTTON DO INCLUDE ---------
    bttn_inserir = Button(formContact, text="Inserir",
                        width=50, command=submitData)
    bttn_inserir.grid(row=6, columnspan=2, pady=10)

def sobreApp():
    pass

# --------- FRAMES TELA PRINCIPAL -------------
top = Frame(root, width=500, bd=1,relief=SOLID)
top.pack(side=TOP)
mid = Frame(root, width=500, bg="#81F781")
mid.pack(side=TOP)
midLeft = Frame(mid, width=100)
midLeft.pack(side=LEFT)
midLeftPadding = Frame(mid, width=350, bg="#81F781")
midLeftPadding.pack(side=LEFT)
midRight = Frame(mid, width=100)
midRight.pack(side=RIGHT)
bottom = Frame(root, width=200)
bottom.pack(side=BOTTOM)
tableMargim = Frame(root, width=500)
tableMargim.pack(side=TOP)


# --------- LABELS TELA PRINCIPAL -------------
lbl_title = Label(top, text="Grade de matérias de Luciano", font='arial 18 bold italic', width=500) 
lbl_title.pack(fill=X)

lbl_alt = Label(bottom, text="Para alterar clique duas vezes no contato desejado.", font=('arial', 12), width=200)
lbl_alt.pack(fill=X)

# --------- BUTTONS TELA PRINCIPAL -------------
bttn_add = Button(midLeft, text="Inserir", bg="OliveDrab1", command=inserirData)
bttn_add.pack()
bttn_del = Button(midRight, text="Deletar",
                 bg="orange red", command=deletarData)
bttn_del.pack(side=RIGHT)

# --------- TREEVIEW TELA PRINCIPAL -------------

scrollbarX = Scrollbar(tableMargim, orient=HORIZONTAL)
scrollbarY = Scrollbar(tableMargim, orient=VERTICAL)

tree = ttk.Treeview(tableMargim, columns=("id", "Nome", "AV", "AV2", "AV3", "AVD", "AVDS", "Média", "Situação"), height=400, 
                    selectmode="extended", yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
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
tree.column('#3', stretch=NO, minwidth=0, width=60)
tree.column('#4', stretch=NO, minwidth=0, width=60)
tree.column('#5', stretch=NO, minwidth=0, width=60)
tree.column('#6', stretch=NO, minwidth=0, width=60)
tree.column('#7', stretch=NO, minwidth=0, width=60)
tree.column('#8', stretch=NO, minwidth=0, width=60)
tree.column('#9', stretch=NO, minwidth=0, width=150)
tree.pack()
tree.bind('<Double-Button-1>', onSelect)

# ----------------- CRIANDO MENU -----------------
menu_bar = Menu(root)
root.config(menu=menu_bar)

# construir o menu
fileMenu = Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label="Menu", menu=fileMenu)
fileMenu.add_command(label="Criar Novo", command=inserirData)
fileMenu.add_separator()
fileMenu.add_command(label="Sair", command=root.destroy)

# construindo outro
menuSobre = Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label="Sobre", menu=menuSobre)
menuSobre.add_command(label="Info", command=sobreApp)


#----------INICIANDO -------------
if __name__ == '__main__':
    database()
    root.mainloop()
