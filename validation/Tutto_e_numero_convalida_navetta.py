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
db_table = "Navetta"    #Table name in MySQL database

# --- END OF MySQL CONFIGURATION ---

# --- COUPON VALIDATION FUNCTION ---

def validate(event):
    bu1.configure (text="")
    bu1.update()
    status.configure(text="AVVICINARE CHIP", background="#8af2fc")
    status.update()
    db = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_name)   #Establish a MySQL database connection
    cless = nfc.ContactlessFrontend("usb")  #Establish a USB connection with the reader device
    ID = StringVar()                        #Make the ID entry as a string format
    tag = cless.connect(rdwr={'on-connect': lambda tag: False})     #Read the Unique ID (UID) of the NFC tag
    beep = cless.connect(rdwr={'beep-on-connect':True})     #Enable beeping for near device communication
    ID = tag.identifier.encode("hex")                       #Convert UID to hex base
    cless.close()  
    name.configure (text= "Braccialetto: %s" % (ID))
    name.update()
    cursor = db.cursor()
    cursor.execute("SELECT ID_Bracelet FROM %s WHERE ID_Bracelet = '%s'" % (db_table, ID))
    results = cursor.fetchall()
    if cursor.rowcount == 0:
        status.configure(text="NOT VALID", background="red")
        status.update()
    else:
        status.configure(text="VALID", background="green")
        status.update()
        cursor.execute("SELECT Nome FROM %s WHERE ID_Bracelet = '%s'" % (db_table, ID))
        results = cursor.fetchall()
        for row in results:
            firstname = row[0]
        cursor.execute("SELECT Cognome FROM %s WHERE ID_Bracelet = '%s'" % (db_table, ID))
        results = cursor.fetchall()
        for row in results:
            surname = row[0]
        client.configure(text="Cliente: %s %s" % (firstname, surname))
        client.update()
    cursor.close()
    db.close()
    clear_textbox()

# --- END OF COUPON VALIDATION FUNCTION ---

# --- TEXTBOX CLEARING ---


def clear_textbox():
    sleep(0.7)
    status.configure(text="IN ATTESA", background="#cedbef")
    b1.delete(0, END)
    bu1.configure (text="Convalida")
    bu1.update
    name.configure(text="Braccialetto:")
    name.update()
    client.configure(text="Cliente:")
    client.update()

# --- END OF TEXTBOX CLEARING ---


# --- GRAPHIC INTERFACE DEFINITION ---
app = Tk()
app.title("Tutto e" + u'\u0300' +" Numero 2019 - Convalidatore Navetta")
app.geometry("900x800+200+100")

title = Label (app, text="Tutto e' Numero 2019", font=("Bahnschrift", 50), fg="#2077bf").pack(padx = 5, pady =0) #Title

row1 = Label(app, text = "Convalida Navetta", font=("Bahnschrift", 35), fg="#000000").pack(padx = 20, pady = 0) #First text row

bv = StringVar()    #bv variable

b1 = Entry(app, textvariable=bv, font=("Bahnschrift", 44)) #Entry box
b1.pack(padx = 20, pady = 15)
b1.focus_force()

status = Label(app, text="IN ATTESA", font=("Bahnschrift", 35), background="#cedbef")
status.pack(padx = 20, pady = 30)

name = Label(app, text="Braccialetto: ", font=("Bahnschrift", 28))
name.pack(pady = 5)

b1.bind("<Return>", validate)

client = Label(app, text="Cliente: ", font=("Bahnschrift", 25))
client.pack(padx = 20, pady = 20)

bu1 = Button(app, text="Convalida", font=("Bahnschrift", 30))
bu1.pack(padx = 20, pady = 20)
bu1.bind("<Button-1>", validate)
bu1.bind("<Return>", validate)

quitter = Button(app, text="Esci", font=("Bahnschrift", 30), command = quit)
quitter.pack(padx = 5, pady = 5)

app.mainloop()