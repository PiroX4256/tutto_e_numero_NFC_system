    # /// Code entirely realized by Luca Pirovano \\\
    # /// Contact me for your projects \\\
    # /// www.lucapirovano.com || contact@lucapirovano.com \\\

import nfc
import mysql.connector
from Tkinter import *
from time import *

    # --- MySQL CONFIGURATION ---
    # --- IMPORTANT: Please insert your MySQL Server login data, in order to establish a connection to the server
db_host = "13.94.187.146"        #Database hostname
db_name = "tuttoenumero"        #Database name
db_user = "tuttoenumero"        #Database login user
db_password = "giugno98"    #Database login password
db_table_pasti = "Buoni_pasto"    #Database table
db_table_navetta = "Navetta"

    # --- END OF MySQL CONFIGURATION ---

    # --- VALIDATE FUNCTION ---

def unlink (event):
    b1.configure(text="Attendere...", background="#ffffff")
    b1.unbind("<Button-1>")
    b1.update()
    db = mysql.connector.connect(user = db_user, password = db_password, host = db_host, database = db_name)
    status.configure(text="AVVICINARE CHIP", background="#8afcfc")
    status.update()

    cless = nfc.ContactlessFrontend("usb")
    tag = cless.connect(rdwr={'on-connect': lambda tag: False})
    beep = cless.connect(rdwr={'beep-on-connect': True})
    cless.close()
    ID = tag.identifier.encode("hex")
    print ID

    cursor = db.cursor()
    cursor.execute("SELECT REG FROM %s WHERE ID_Bracelet='%s'" % (db_table_pasti, ID))
    results = cursor.fetchall()
    print results
    if cursor.rowcount == 0:
        status.configure(text="PASTO: ID non trovato", background="#d34343")
        status.update()
        sleep(1)
    else:
        cursor.execute("UPDATE %s SET REG=0 WHERE ID_Bracelet = '%s'" % (db_table_pasti, ID))
        db.commit()
        cursor.execute("SELECT Nome FROM %s WHERE ID_Bracelet = '%s'" % (db_table_pasti, ID))
        name = cursor.fetchall()
        cursor.execute("SELECT Cognome FROM %s WHERE ID_Bracelet ='%s'" % (db_table_pasti, ID))
        surname = cursor.fetchall()
        for row in name:
            name = row[0]
        for row in surname:
            surname = row[0]
        client.configure(text="Cliente: %s %s" % (name, surname))
        client.update()
        order.configure(text="Braccialetto: %s" % (ID))
        order.update()
        cursor.execute("SELECT ID_Bracelet FROM %s WHERE ID_Bracelet='%s'" % (db_table_pasti, ID))
        results3 = cursor.fetchall()
        cursor.execute("UPDATE %s SET ID_Bracelet=NULL WHERE ID_Bracelet = '%s'" % (db_table_pasti, ID))
        db.commit()
        status.configure(text="PASTO: BRACCIALETTO RIMOSSO DAL SISTEMA", background="#289b22")
        status.update()
        sleep(2)

    cursor.execute ("SELECT REG FROM %s WHERE ID_Bracelet='%s'" % (db_table_navetta, ID))
    results_navetta = cursor.fetchall()
    if cursor.rowcount == 0:
        status.configure(text="NAVETTA: ID non trovato", background="#d34343")
        status.update()
        sleep(1)

    else:
        cursor.execute("SELECT Nome FROM %s WHERE ID_Bracelet = '%s'" % (db_table_navetta, ID))
        name = cursor.fetchall()
        cursor.execute("SELECT Cognome FROM %s WHERE ID_Bracelet ='%s'" % (db_table_navetta, ID))
        surname = cursor.fetchall()
        for row in name:
            name = row[0]
        for row in surname:
            surname = row[0]
        client.configure(text="Cliente: %s %s" % (name, surname))
        client.update()
        cursor.execute("UPDATE %s SET REG=0 WHERE ID_Bracelet = '%s'" % (db_table_navetta, ID))
        db.commit()
        cursor.execute("UPDATE %s SET ID_Bracelet=NULL WHERE ID_Bracelet = '%s'" % (db_table_navetta, ID))
        db.commit()
        status.configure(text="NAVETTA: BRACCIALETTO RIMOSSO DAL SISTEMA", background="#289b22")
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
    b1.configure(text="DISSOCIA", background="#f29e4f")
    b1.bind("<Button-1>", unlink)
    b1.update()
    client.configure(text="Cliente: ")
    client.update()
    order.configure(text="Braccialetto: ")
    order.update()

    # --- END OF CLEARING FUNCTION ---

    # --- QUIT FUNCTION ---

def quit():
    app.destroy()

    # --- END OF QUIT FUNCTION ---

    # --- APPLICATION INTERFACE ---
app = Tk()
app.title("Tutto e" + u'\u0300' +" Numero 2019 - Check-in")
app.geometry("1200x850+250+90")

entrypass = StringVar()

title = Label (app, text="Tutto e" + u'\u0300' +" Numero 2019 | Check-out", font=("Bahnschrift", 45), fg="#2077bf").pack(padx = 5, pady =0) #Title

row1 = Label(app, text = "GENERALE", font=("Bahnschrift", 40), fg="#d34343").pack(padx = 20, pady = 0) #First text row

row2 = Label(app, text = "Cliccare DISSOCIA per iniziare la procedura \n di unlink del braccialetto.", font=("Bahnschrift", 30)).pack(padx = 30, pady = 30) #Second text row

status = Label(app, text= "IN ATTESA", font=("Bahnschrift", 35), background="#4fa1f2") #Status sign
status.pack(padx = 20, pady = 20)
status.focus_force()
status.bind("<Return>", unlink)


b1 = Button(app, text="DISSOCIA", font=("Bahnschrift", 30), background="#B3565A") #Convalidation button
b1.pack(padx=20, pady=20)
b1.bind("<Button-1>", unlink)

client = Label(app, text="Cliente: ", font=("Bahnschrift", 25))
client.pack(padx = 20, pady = 20)

order = Label(app, text="Braccialetto: ", font=("Bahnschrift", 25))
order.pack(padx = 20, pady = 20)

quit = Button(app, text="Esci", font=("Bahnschrift", 25), command = quit)
quit.pack(padx = 20, pady = 20)

app.mainloop()
