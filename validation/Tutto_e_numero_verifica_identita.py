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

db_host = contents[0]        #Database hostname
db_name = "tuttoenumero"        #Database name
db_user = "tuttoenumero"        #Database login user
db_password = "giugno98"    #Database login password
db_table = "Buoni_pasto"    #Database table

    # --- END OF MySQL CONFIGURATION ---

    # --- BRACELET ASSIGNMENT FUNCTION ---

def check(event):
    Check.configure(text="")
    Check.update()
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
    cursor.execute("SELECT Nome FROM %s WHERE ID_Bracelet = '%s'" %(db_table, ID))
    name = cursor.fetchall()
    if cursor.rowcount == 0:
        status.configure (text="ALERT: NESSUNA CORRISPONDENZA", background = "#e8dc86")
        status.update()
        sleep(1.5)
    else:
        cursor.execute("SELECT Cognome FROM %s WHERE ID_Bracelet = '%s'" %(db_table, ID))
        surname = cursor.fetchall()
        for row in name:
            r_name = row[0]
        for row in surname:
            r_surname = row[0]
        status.configure(text="VALIDO", background="green")
        status.update()
        note.configure(text="Note: braccialetto registrato a %s %s" % (r_name, r_surname))
        note.update()
        sleep(2)
    cursor.close()
    db.close()
    clear_fields()

def clear_fields():
    status.configure(text="IN ATTESA", background="#cedbef")
    status.update()
    assigned_id.configure(text="Braccialetto: ")
    assigned_id.update()
    Check.configure(text="CONVALIDA")
    Check.update()
    note.configure(text="Note: ")
    note.update()

    # --- APPLICATION INTERFACE ---

app = Tk()
app.title("Tutto e" + u'\u0300' +" Numero 2019 - Check-in")
app.geometry("1000x650+450+30")

entrypass = StringVar()

title = Label (app, text="Tutto e" + u'\u0300' +" Numero 2019 | Check-in", font=("Bahnschrift", 45), fg="#2077bf").pack(padx = 5, pady =0) #Title

row1 = Label(app, text = "VERIFICA IDENTITA" + u'\u0300' + " BRACCIALETTO", font=("Bahnschrift", 30), fg="#d34343").pack(padx = 20, pady = 0) #First text row

row2 = Label(app, text = "Per iniziare cliccare su CONVALIDA o premere ENTER", font=("Bahnschrift", 24)).pack(padx = 30, pady = 15) #Second text row

status = Label(app, text="IN ATTESA", font=("Bahnschrift", 25), background="#cedbef")
status.pack(pady = 25)
status.focus_force()
status.bind("<Return>", check)

Check = Button(app, text="CONVALIDA", font=("Bahnschrift", 25), background="#8dd6b7")
Check.pack(pady=15)
Check.bind("<Button-1>", check)

assigned_id = Label(app, text="Braccialetto: ", font=("Bahnschrift", 18))
assigned_id.pack(pady=10)

note = Label(app, text="Note: ", font=("Bahnschrift", 18))
note.pack(pady=5)

quitter = Button(text="Esci", font=("Bahnschrift", 20), command=quit).pack(pady=20)

copy = Label(app, text="Luca Pirovano Services | ICT Section | version 1.0.1", font=("Bahnschrift", 12)).pack(pady=10)

app.mainloop()
