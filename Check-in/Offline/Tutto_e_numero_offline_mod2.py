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

db_host = contents[0]        #Database hostname
db_name = "tuttoenumero"        #Database name
db_user = "tuttoenumero"        #Database login user
db_password = "giugno98"    #Database login password
db_table = "Buoni_pasto"    #Database table

    # --- END OF MySQL CONFIGURATION ---

def validate():
    def upload(event):
        # --- BEGIN OF MEAL SELECTION IDENTIFICATION ---
        if MC.get()==1:
            mc = "MC"
        else:
            mc = ""
        if GP.get()==1:
            gp = "GP"
        else:
            gp = ""
        if GC.get()==1:
            gc = "GC"
        else:
            gc = ""
        if VP.get()==1:
            vp = "VP"
        else:
            vp = ""
        if VC.get()==1:
            vc = "VC"
        else:
            vc = ""
        if SP.get()==1:
            sp = "SP"
        else:
            sp = ""
        meal = ("%s %s %s %s %s %s" % (mc, gp, gc, vp, vc, sp))
        print meal
        # --- END OF MEAL SELECTION IDENTIFICATION ---

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
        cursor.execute("SELECT Tipo FROM %s WHERE (Nome, Cognome) = ('%s', '%s')" % (db_table, contents[0], contents[1]))
        already = cursor.fetchall()
        print already
        if cursor.rowcount == 0:
            print "Paolone"
            cursor.execute("SELECT ID_Bracelet FROM %s WHERE ID_Bracelet = '%s'" % (db_table, ID))
            results = cursor.fetchall()
            #print results
            if cursor.rowcount==0:
                cursor.execute("SELECT ID FROM Buoni_pasto")
                results = cursor.fetchall()
                for element in results:
                    print element[0]
                    elemen = element[0] + 1
                print elemen
                cursor.execute("INSERT INTO Buoni_pasto (ID, ID_Bracelet, Nome, Cognome, Tipo, Pasti) VALUES (%s, %s, %s, %s, %s, %s)", (elemen, ID, contents[0], contents[1], "Other", meal))
                db.commit()
                status.configure(text="SUCCESS", background="#289b22")
                status.update()
                sleep(1.5)
            else:
                status.configure(text="ERRORE: BRACCIALETTO GIA" + u'\u0300' + " REGISTRATO \nAD ALTRO NOMINATIVO", background="red", font=("Bahnschrift", 23))
                status.update()
                sleep(2)
        else:
            if "Carnet" in already[0]:
                status.configure(text="ALERT: CARNET GIA" + u'\u0300' + " PRESENTE \nSUL BRACCIALETTO", background="#e8dc86", font=("Bahnschrift", 23))
                status.update()
                sleep(2)
            else:
                cursor.execute("SELECT Nome FROM %s WHERE ID_Bracelet = '%s'" % (db_table, ID))
                ifalreadyname = cursor.fetchall()
                cursor.execute("SELECT Cognome FROM %s WHERE ID_Bracelet = '%s'" % (db_table, ID))
                ifalreadysurname = cursor.fetchall()
                if contents[0] in ifalreadyname[0] and contents[1] in ifalreadysurname[0]:
                    cursor.execute("UPDATE %s SET Pasti = concat(Pasti, concat(',', '%s')) WHERE ID_Bracelet = '%s'" % (db_table, meal, ID))
                    db.commit()
                    status.configure(text="ALERT: BRACCIALETTO GIA" + u'\u0300' + " REGISTRATO\nPASTI AGGIUNTI", background="#e8dc86", font=("Bahnschrift", 23))
                    status.update()                
                else:
                    status.configure(text="ERRORE: BRACCIALETTO/NOMINATIVO\nDISCORDANTI", background="red", font=("Bahnschrift", 23))
                    status.update()
                    sleep(2)
        validation.destroy()
    db = mysql.connector.connect(user = db_user, password = db_password, host = db_host, database = db_name)
    cursor = db.cursor()



    #cursor.execute("SELECT ID FROM Buoni_pasto")
    #results = cursor.fetchall()
    #for element in results:
        #print element[0]
        #elemen = element[0] + 1
    #print elemen
    #cursor.execute("INSERT INTO Buoni_pasto (ID, Nome, Cognome, Tipo) VALUES (%s, %s, %s, %s)", (elemen, contents[0], contents[1], "Other"))
    #db.commit()
    cursor.close()
    db.close()
    sel.destroy()
    validation = Tk()
    validation.title("Caricamento del buono...")
    validation.geometry("600x230+700+300")
    validation.focus_force()
    row11= Label(validation, text="Inserire i dati, premere ENTER e \n posizionare il braccialetto sul lettore", font=("Bahnschrift", 16)).pack(pady=10)
    status = Label(validation, text= "IN ATTESA", font=("Bahnschrift", 35), background="#4fa1f2")
    status.pack(pady=35)
    status.bind("<Return>", upload)
    status.focus_force()
    validation.mainloop()
    f = open("variables.txt", "w+")
    f.close()

sel = Tk()
sel.title("Seleziona")
sel.geometry("230x120+800+400")

f = open("variables.txt", "r")
contents = f.read().splitlines()
print (contents[0], contents[1])
f.close()

MC= IntVar()
GP = IntVar()
GC = IntVar()
VP = IntVar()
VC = IntVar()
SP = IntVar()


Checkbutton(sel, text="Mercoledi Cena", font=("Bahnschrift", 10), variable=MC).grid(row=1, sticky=W)    #Selection ticks
Checkbutton(sel, text="Giovedi Pranzo", font=("Bahnschrift", 10), variable=GP).grid(row=2, sticky=W)
Checkbutton(sel, text="Giovedi Cena", font=("Bahnschrift", 10), variable=GC).grid(row=2, column=2, sticky=W)
Checkbutton(sel, text="Venerdi Pranzo", font=("Bahnschrift", 10), variable=VP).grid(row=3, sticky=W)
Checkbutton(sel, text="Venerdi Cena", font=("Bahnschrift", 10), variable=VC).grid(row=3, column=2, sticky=W)
Checkbutton(sel, text="Sabato Pranzo", font=("Bahnschrift", 10), variable=SP).grid(row=3, column=2, sticky=W)

Button(sel, text='Carica', command=validate, font=("Bahnschrift", 12)).grid(row=4, sticky=W, pady=4, padx=5)    #Confirmation button
sel.mainloop()