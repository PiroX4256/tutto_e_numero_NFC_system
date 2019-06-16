    # /// Code entirely realized by Luca Pirovano \\\
    # /// Contact me for your projects \\\
    # /// www.lucapirovano.com || contact@lucapirovano.com \\\

import nfc
import mysql.connector
from Tkinter import *
from time import *

    # --- MySQL CONFIGURATION ---
    # --- IMPORTANT: Please insert your MySQL Server login data, in order to establish a connection to the server
f = open("address.txt", "r")
contents = f.read().splitlines()
print contents[0]
f.close()

db_host = contents[0]         #Database hostname
db_name = "tuttoenumero"        #Database name
db_user = "tuttoenumero"        #Database login user
db_password = "giugno98"    #Database login password
db_table = "Buoni_pasto"    #Database table

    # --- END OF MySQL CONFIGURATION ---

    # --- BRACELET ASSIGNMENT FUNCTION ---

def assign(event):
    status.configure(text="AVVICINARE CHIP", background="#8af2fc")
    status.update()
    db = mysql.connector.connect(user = db_user, password = db_password, host = db_host, database = db_name)
    cursor = db.cursor()
    cless = nfc.ContactlessFrontend("usb")
    tag = cless.connect(rdwr={'on-connect': lambda tag: False})
    beep = cless.connect(rdwr={'beep-on-connect': True})
    cless.close()
    ID = tag.identifier.encode("hex")
    assigned_id.configure(text="Braccialetto: %s" % (ID))
    assigned_id.update()
    cursor.execute("SELECT ID_Bracelet FROM %s WHERE ID_Bracelet = '%s'" %(db_table, ID))
    ids = cursor.fetchall()
    if cursor.rowcount == 0:
        print "Paolino"
        cursor.execute("SELECT ID FROM Buoni_pasto")
        results = cursor.fetchall()
        for element in results:
            print element[0]
            elemen = element[0] + 1
        print elemen
        cursor.execute("INSERT INTO Buoni_pasto (ID, ID_Bracelet, Nome, Cognome) VALUES (%s, %s, %s, %s)", (elemen, ID, name.get(), surname.get()))
        db.commit()
        status.configure (text="SUCCESS", background = "green")
        status.update()
        sleep(1.5)
    else:
        status.configure(text="ERRORE: BRACCIALETTO GIA" + u'\u0300' + " ASSEGNATO", background="red")
        status.update()
        sleep(2)
    cursor.close()
    db.close()
    clear_fields()

def clear_fields():
    e1.delete(0, END)
    e2.delete(0, END)
    status.configure(text="IN ATTESA", background="#cedbef")
    status.update()
    assigned_id.configure(text="Braccialetto: ")
    assigned_id.update()
    e1.focus_force()

    # --- APPLICATION INTERFACE ---

app = Tk()
app.title("Tutto e" + u'\u0300' +" Numero 2019 - Check-in")
app.geometry("1000x720+450+30")

entrypass = StringVar()

title = Label (app, text="Tutto e" + u'\u0300' +" Numero 2019 | Check-in", font=("Bahnschrift", 45), fg="#2077bf").pack(padx = 5, pady =0) #Title

row1 = Label(app, text = "ASSEGNAZIONE BRACCIALETTO SENZA SERVIZI", font=("Bahnschrift", 30), fg="#d34343").pack(padx = 20, pady = 0) #First text row

row2 = Label(app, text = "Inserire il nominativo e cliccare sul tasto ASSEGNA", font=("Bahnschrift", 24)).pack(padx = 30, pady = 15) #Second text row

name = StringVar()
surname = StringVar()

Label(app, text="Nome", font=("Bahnschrift", 16)).pack(pady=5)
e1 = Entry(app, textvariable=name, font=("Bahnschrift", 16))
e1.pack(pady=5)
e1.focus_force()
Label(app, text="Cognome", font=("Bahnschridt", 16)).pack(pady=5)
e2 = Entry(app, textvariable=surname, font=("Bahnschrift", 16))
e2.pack(pady=5)
e2.bind("<Return>", assign)

status = Label(app, text="IN ATTESA", font=("Bahnschrift", 30), background="#cedbef")
status.pack(pady = 25)

Assign = Button(app, text="ASSEGNA", font=("Bahnschrift", 18), command=assign, background="#f29e4f")
Assign.pack(pady=15)
Assign.bind("<Button-1>", assign)

assigned_id = Label(app, text="Braccialetto: ", font=("Bahnschrift", 25))
assigned_id.pack(pady=10)

quitter = Button(text="Esci", font=("Bahnschrift", 20), command=quit).pack(pady=20)

copy = Label(app, text="Luca Pirovano Services | ICT Section | version 1.0.1", font=("Bahnschrift", 12)).pack(pady=10)

app.mainloop()