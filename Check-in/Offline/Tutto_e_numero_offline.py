    # /// Code entirely realized by Luca Pirovano \\\
    # /// Contact me for your projects \\\
    # /// www.lucapirovano.com || contact@lucapirovano.com \\\

import nfc
import mysql.connector
from Tkinter import *
from time import *
import os
import datetime

    # --- MySQL CONFIGURATION ---
    # --- IMPORTANT: Please insert your MySQL Server login data, in order to establish a connection to the server
f = open("address.txt", "r")
contents = f.read().splitlines()
print contents[0]
f.close()

db_host = contents[0]       #Database hostname
db_name = "tuttoenumero"        #Database name
db_user = "tuttoenumero"        #Database login user
db_password = "giugno98"    #Database login password
db_table = "Buoni_pasto"    #Database table
db_table_navetta = "Navetta"    #Database nav table

    # --- END OF MySQL CONFIGURATION ---

def Single():
    global MC
    def validate():
        global MC
        print (MC.get(), GP.get(), GC.get())
        print("MC: %s,\nGP: %d" % (MC.get(), VP.get()))
        sel.destroy()
    sel = Tk()
    sel.title("Seleziona")
    sel.geometry("230x120+800+400")

    prova = IntVar()
    MC= IntVar()
    GP = IntVar()
    GC = IntVar()
    VP = IntVar()
    VC = IntVar()

    Checkbutton(sel, text="Mercoledi Cena", font=("Bahnschrift", 10), variable=MC).grid(row=1, sticky=W)    #Selection ticks
    Checkbutton(sel, text="Giovedi Pranzo", font=("Bahnschrift", 10), variable=GP).grid(row=2, sticky=W)
    Checkbutton(sel, text="Giovedi Cena", font=("Bahnschrift", 10), variable=GC).grid(row=2, column=2, sticky=W)
    Checkbutton(sel, text="Venerdi Pranzo", font=("Bahnschrift", 10), variable=VP).grid(row=3, sticky=W)
    Checkbutton(sel, text="Venerdi Cena", font=("Bahnschrift", 10), variable=VC).grid(row=3, column=2, sticky=W)

    Button(sel, text='Carica', command=validate, font=("Bahnschrift", 12)).grid(row=4, sticky=W, pady=4, padx=5)    #Confirmation button
    sel.mainloop()

    # --- CARNET FUNCTION ---

def Carnet ():
    def upload(event):
        name_db = name.get()
        surname_db = surname.get()
        status.configure(text="AVVICINARE CHIP", background="#8afcfc")
        status.update()
        cless = nfc.ContactlessFrontend("usb")
        #----------------
        def undo_cless():
            cless.close()
            validation.destroy()
        #------------------------
        tag = cless.connect(rdwr={'on-connect': lambda tag: False})
        #beep = cless.connect(rdwr={'beep-on-connect': True})
        cless.close()
        ID = tag.identifier.encode("hex")
        #print ID
        db = mysql.connector.connect(user = db_user, password = db_password, host = db_host, database = db_name)
        cursor = db.cursor()

        cursor.execute("SELECT ID_Bracelet FROM %s WHERE (Nome, Cognome) = ('%s', '%s')" % (db_table, name_db, surname_db))
        already = cursor.fetchall()
        if cursor.rowcount == 0:
            print "Paolino"
            cursor.execute("SELECT ID_Bracelet FROM %s WHERE ID_Bracelet = '%s'" % (db_table, ID))
            results = cursor.fetchall()
            if cursor.rowcount==0:
                cursor.execute("SELECT ID FROM Buoni_pasto")
                results = cursor.fetchall()
                for element in results:
                    print element[0]
                    elemen = element[0] + 1
                print elemen
                cursor.execute("INSERT INTO Buoni_pasto (ID, ID_Bracelet, Nome, Cognome, Tipo) VALUES (%s, %s, %s, %s, %s)", (elemen, ID, name.get(), surname.get(), "Carnet"))
                db.commit()
                status.configure(text="SUCCESS", background="#289b22")
                status.update()
                sleep(1.5)
            else:
                status.configure(text="ERRORE: BRACCIALETTO GIA" + u'\u0300' + " REGISTRATO", background="red", font=("Bahnschrift", 23))
                status.update()
                sleep(1.5)
        else:
            sleep(2)
            print "Paolone"
            print already
            for rows in already:
                if ID in rows[0]:
                    cursor.execute("UPDATE %s SET Tipo = '%s' WHERE ID_Bracelet='%s'" % (db_table, "Carnet", ID))
                    db.commit()
                    status.configure(text="SUCCESS", background="#289b22")
                    status.update()
                else:
                    status.configure(text="ERRORE: BRACCIALETTO/NOMINATIVO\nDISCORDANTI", background="red", font=("Bahnschrift", 23))
                    status.update()


            sleep(1.5)
            print "CIao"

        cursor.close()
        db.close()
        e1.delete(0, END)
        e2.delete(0, END)
        e1.focus_force()
        validation.destroy()
    validation = Tk()
    validation.title("Caricamento del buono...")
    validation.geometry("600x230+700+300")
    validation.focus_force()
    row11= Label(validation, text="Inserire i dati, premere ENTER e \n posizionare il braccialetto sul lettore", font=("Bahnschrift", 16)).pack(pady=10)
    status = Label(validation, text= "IN ATTESA", font=("Bahnschrift", 35), background="#4fa1f2")
    status.pack(pady=35)
    status.bind("<Return>", upload)
    status.focus_force()
    if name.get()=="" or surname.get()=="":
        print "error"
        status.configure(text="ERRORE: INSERIRE NOME E COGNOME", background="red", font=("Bahnschrift", 23))
        status.update()
        sleep(1.5)
        validation.destroy()
    validation.mainloop()
    

    # --- END OF THE CARNET FUNCTION ---

    # --- QUIT FUNCTION ---

def quit():
    app.destroy()

    # --- END OF QUIT FUNCTION ---


    # --- SINGLE MEAL FUNCTION ---

def Other():
    print name.get(), surname.get()
    if name.get()=="" or surname.get()=="":
        print "Errore: inserire i dati richiesti"
    else:
        f = open("variables.txt", "w+")
        f.write("%s\n" % name.get())
        f.write("%s" % surname.get())
        f.close()
        e1.delete(0, END)
        e2.delete(0, END)
        e1.focus_force()
        os.system('python "%s/Tutto_e_numero_offline_mod2.py"' % (dir_path))
        e1.delete(0, END)
        e2.delete(0, END)
        e1.focus_force()

    # --- END OF SINGLE MEAL FUNCTION ---

    # --- BUS SERVICE FUNCTION ---
def Nav():
    def upload(event):
        name_db = name.get()
        surname_db = surname.get()
        status.configure(text="AVVICINARE CHIP", background="#8afcfc")
        status.update()
        cless = nfc.ContactlessFrontend("usb")
        #----------------
        def undo_cless():
            cless.close()
            validation.destroy()
        #------------------------
        tag = cless.connect(rdwr={'on-connect': lambda tag: False})
        #beep = cless.connect(rdwr={'beep-on-connect': True})
        cless.close()
        ID = tag.identifier.encode("hex")
        #print ID
        db = mysql.connector.connect(user = db_user, password = db_password, host = db_host, database = db_name)
        cursor = db.cursor()
        cursor.execute("SELECT ID_Bracelet FROM %s WHERE ID_Bracelet = '%s'" % (db_table_navetta, ID))
        results = cursor.fetchall()
        #print results
        if cursor.rowcount==0:
            cursor.execute("SELECT ID FROM %s" % (db_table_navetta))
            results = cursor.fetchall()
            for element in results:
                print element[0]
                elemen = element[0] + 1
            print elemen
            cursor.execute("INSERT INTO Navetta (ID, ID_Bracelet, Nome, Cognome) VALUES (%s, %s, %s, %s)", (elemen, ID, name.get(), surname.get()))
            db.commit()
            status.configure(text="SUCCESS", background="#289b22")
            status.update()
            e1.delete(0, END)
            e2.delete(0, END)
            sleep(1.5)
        else:
            status.configure(text="ERRORE: BRACCIALETTO GIA" + u'\u0300' + " REGISTRATO", background="red", font=("Bahnschrift", 23))
            status.update()
            e1.delete(0, END)
            e2.delete(0, END)
            sleep(1.5)
        cursor.close()
        db.close()
        validation.destroy()
        e1.delete(0, END)
        e2.delete(0, END)
        e1.focus_force()
    validation = Tk()
    validation.title("Caricamento del buono...")
    validation.geometry("600x200+700+300")
    validation.focus_force()
    row11= Label(validation, text="Inserire i dati, premere ENTER e \n posizionare il braccialetto sul lettore", font=("Bahnschrift", 16)).pack(pady=10)
    status = Label(validation, text= "IN ATTESA", font=("Bahnschrift", 35), background="#4fa1f2")
    status.pack(pady=35)
    status.bind("<Return>", upload)
    status.focus_force()
    if name.get()=="" or surname.get()=="":
        print "error"
        status.configure(text="ERRORE: INSERIRE NOME E COGNOME", background="red", font=("Bahnschrift", 23))
        status.update()
        sleep(1.5)
        validation.destroy()
    validation.mainloop()

    # --- END OF BUS SERVICE FUNCTION ---

    # --- APPLICATION INTERFACE ---
app = Tk()
app.title("Tutto e" + u'\u0300' +" Numero 2019 - Check-in")
app.geometry("1000x950+450+30")

entrypass = StringVar()

title = Label (app, text="Tutto e" + u'\u0300' +" Numero 2019 | Check-in", font=("Bahnschrift", 45), fg="#2077bf").pack(padx = 5, pady =0) #Title

row1 = Label(app, text = "ACQUISTO OFFLINE", font=("Bahnschrift", 40), fg="#d34343").pack(padx = 20, pady = 0) #First text row

row2 = Label(app, text = "Selezionare il tipo di buono da caricare e\ninserire il nominativo", font=("Bahnschrift", 24)).pack(padx = 30, pady = 15) #Second text row

dir_path = os.path.dirname(os.path.realpath(__file__))

Label(app, text="BUONI PASTO", font=("Bahnschrift", 30)).pack(pady=5)
Carnet = Button(app, text="Carnet", font=("Bahnschrift", 18), command=Carnet, background="#f29e4f").pack(pady=10)
Other = Button(text="Pasti Singoli", font=("Bahnschrift", 18), command=Other, background="#4fa1f2").pack(pady=10)

Label(app, text="NAVETTA", font=("Bahnschrift", 30)).pack(pady=10)
nav = Button(app, text="Navetta (all days)", font=("Bahnschrift", 18), background="#d9db7d", command=Nav).pack(pady=10)

name = StringVar()
surname = StringVar()

Label(app, text="Nome", font=("Bahnschrift", 16)).pack(pady=5)
e1 = Entry(app, textvariable=name, font=("Bahnschrift", 16))
e1.pack(pady=5)
e1.focus_force()
Label(app, text="Cognome", font=("Bahnschridt", 16)).pack(pady=5)
e2 = Entry(app, textvariable=surname, font=("Bahnschrift", 16))
e2.pack(pady=5)

quitter = Button(text="Esci", font=("Bahnschrift", 20), command=quit).pack(pady=40)

copy = Label(app, text="Luca Pirovano Services | ICT Section | version 1.1.1", font=("Bahnschrift", 12)).pack(pady=10)

app.mainloop()