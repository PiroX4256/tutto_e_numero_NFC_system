# /// Code entirely realized by Luca Pirovano \\\
# /// Contact me for your projects \\\
# /// www.lucapirovano.com || contact@lucapirovano.com \\\

import nfc
import mysql.connector
from Tkinter import *
from time import *

# --- MySQL CONFIGURATION ---
# --- IMPORTANT: Please insert your MySQL Server login data, in order to establish a connection to the server
db_host = ""        #Database hostname
db_name = ""        #Database name
db_user = ""        #Database login user
db_password = ""    #Database login password
db_table = ""    #Database table

# --- END OF MySQL CONFIGURATION ---

# --- VALIDATE FUNCTION ---

def validate (event):
    entry = entrypass.get()
    print entry
    b1.configure(text="Attendere...", background="#ffffff")
    b1.unbind("<Button-1>")
    b1.update()
    db = mysql.connector.connect(user = db_user, password = db_password, host = db_host, database = db_name)
    cursor = db.cursor()
    cursor.execute("SELECT Nome FROM %s WHERE ID='%s'" % (db_table, entry))
    name = cursor.fetchall()
    if cursor.rowcount == 0:
        status.configure(text="ERRORE: ID non trovato", background="#d34343")
        status.update()
        sleep(2)
    else:
        for row in name:
            name = row[0]
        cursor.execute("SELECT Cognome FROM %s WHERE ID='%s'" % (db_table, entry))
        surname = cursor.fetchall()
        for row in surname:
            surname = row[0]
        client.configure(text="Cliente: %s %s" % (name, surname))
        client.update()
        order.configure(text="Ordine: %s" % (entry))
        order.update()
        cursor.execute("SELECT REG FROM %s WHERE ID='%s'" % (db_table, entry))
        checkreg = cursor.fetchall()

        for row in checkreg:
            checkreg = row[0]
        print checkreg
        if checkreg == 1:
            status.configure(text="ERRORE: ID gia" + u'\u0300' +" registrato", background="#d34343")
            status.update()
            sleep(2)
        else:
            status.configure(text="AVVICINARE CHIP", background="#8afcfc")
            status.update()
            ID = StringVar()
            cless = nfc.ContactlessFrontend("usb") #Establish a USB connection to NFC reader
            tag = cless.connect (rdwr={'on-connect': lambda tag: False})  
            beep = cless.connect(rdwr={'beep-on-connect': True})
            cless.close()
            ID = tag.identifier.encode("hex")
            print ID
            cursor.execute("SELECT ID_Bracelet FROM %s WHERE ID_Bracelet='%s'" % (db_table, ID))
            bracelet_check = cursor.fetchall()
            if cursor.rowcount == 0:
                cursor.execute("UPDATE %s SET ID_Bracelet='%s' WHERE ID ='%s'" % (db_table, ID, entry))
                db.commit()
                cursor.execute("UPDATE %s SET REG=1 WHERE ID = '%s'" % (db_table, entry))
                db.commit()
                status.configure(text="SUCCESS", background="#289b22")
                status.update()
                client.configure(text="Braccialetto %s registrato a %s %s" % (ID, name, surname))
                client.update()
                sleep(2)
            else:
                cursor.execute("SELECT Nome FROM %s WHERE ID_Bracelet = '%s'" % (db_table, ID))
                namealready = cursor.fetchall()
                cursor.execute("SELECT Cognome FROM %s WHERE ID_Bracelet ='%s'" % (db_table, ID))
                surnamealready = cursor.fetchall()
                for row in namealready:
                    namealready = row[0]
                for row in surnamealready:
                    surnamealready = row[0]
                client.configure(text="Braccialetto %s " %(ID) + "gia" + u'\u0300' +" registrato a %s %s" % (namealready, surnamealready))
                client.update()
                status.configure(text="ERRORE: Braccialetto gia" + u'\u0300' +" registrato")
                status.update()
                sleep(2)
    db.close()
    clear_textbox()


# --- END OF THE VALIDATION FUNCTION ---

# --- FUNCTION FOR TEXTBOX CLEARING ---

def clear_textbox():
    sleep(0.7)
    status.configure(text="IN ATTESA", background="#4fa1f2")
    status.update()
    entry.delete(0, END)
    b1.configure(text="Convalida", background="#f29e4f")
    b1.bind("<Button-1>", validate)
    b1.update()
    client.configure(text="Cliente: ")
    client.update()
    order.configure(text="Ordine: ")
    order.update()

# --- END OF CLEARING FUNCTION ---

# --- QUIT FUNCTION ---

def quit():
    app.destroy()

# --- END OF QUIT FUNCTION ---

# --- APPLICATION INTERFACE ---
app = Tk()
app.title("Tutto e' Numero 2019 - Check-in")
app.geometry("1000x900+450+50")

entrypass = StringVar()

title = Label (app, text="Tutto e" + u'\u0300' +" Numero 2019 | Check-in", font=("Bahnschrift", 45), fg="#2077bf").pack(padx = 5, pady =0) #Title

row1 = Label(app, text = "BUONI PASTO", font=("Bahnschrift", 40), fg="#d34343").pack(padx = 20, pady = 0) #First text row

row2 = Label(app, text = "Inserire ID buono", font=("Bahnschrift", 30)).pack(padx = 30, pady = 30) #Second text row

entry = Entry(app, textvariable=entrypass,font=("Bahnschrift", 44)) #Entry textbox for order number
entry.pack(padx = 20, pady = 20)
entry.focus_force()
entry.bind("<Return>", validate)

status = Label(app, text= "IN ATTESA", font=("Bahnschrift", 35), background="#4fa1f2") #Status sign
status.pack(padx = 20, pady = 20)

b1 = Button(app, text="Convalida", font=("Bahnschrift", 30), background="#f29e4f") #Convalidation button
b1.pack(padx=20, pady=20)
b1.bind("<Button-1>", validate)

client = Label(app, text="Cliente: ", font=("Bahnschrift", 25))
client.pack(padx = 20, pady = 20)

order = Label(app, text="Ordine: ", font=("Bahnschrift", 25))
order.pack(padx = 20, pady = 20)

quit = Button(app, text="Esci", font=("Bahnschrift", 25), command = quit)
quit.pack(padx = 20, pady = 20)
app.mainloop()
