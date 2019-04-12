# /// Code entirely realized by Luca Pirovano \\\
# /// Contact me for your projects \\\
# /// www.lucapirovano.com || contact@lucapirovano.com \\\

import mysql.connector
from time import *
from Tkinter import *
import nfc
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
db_table = "Buoni_pasto"    #Table name in MySQL database

# --- END OF MySQL CONFIGURATION ---

# ---*** BOOT PARAMETERS ***--- #

day = input("\n\nPer favore inserire l'ID del pasto. Puoi trovare gli ID corrispondenti qui sotto.\n -----ID----\n 1.MERCOLEDI CENA\n 2.GIOVEDI PRANZO \n 3.GIOVEDI CENA \n 4.VENERDI PRANZO \n 5.VENERDI CENA \n  Scelta: ")
if day>5:
    print ("Devi inserire un numero compreso tra 1 e 5. \nIl programma verra' ora automaticamente chiuso.")
    sleep(3)
    quit()

elif day<1:
    print ("Devi inserire un numero compreso tra 1 e 5. \nIl programma verra' ora automaticamente chiuso.")
    sleep(3)
    quit()

machine = input("\n\nPer favore inserire l'ID macchina. Puoi trovare gli ID corrispondenti qui sotto.\n ----IDs----\n 1.BANCO PRIMI\n 2.BANCO SECONDI\n 3.FRUTTA / DESSERT\n   Scelta: ")
if machine>3:
    print ("Devi inserire un numero compreso tra 1 e 3. \nIl programma verra' ora automaticamente chiuso.")
    sleep(3)
    quit()

elif machine<1:
    print ("Devi inserire un numero compreso tra 1 e 3. \nIl programma verra' ora automaticamente chiuso.")
    sleep(3)
    quit()
#=============================================================================


#=============================================================================
# --- COUPON VALIDATION FUNCTION ---

def validate(event):
    bu1.configure (text="")
    bu1.update()
    status.configure(text="AVVICINARE CHIP", background="#8af2fc")
    status.update()
    db = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_name)   #Establish a MySQL database connection
    cless = nfc.ContactlessFrontend("usb")  #Establish a USB connection with the reader device

    if day== 1:                             #Link all meals to their definition // used during validation
        meal = "MercolediCENA"
        kw = "MC"
    elif day==2:
        meal = "GiovediPRANZO"
        kw = "GP"
    elif day==3:
        meal = "GiovediCENA"
        kw = "GC"
    elif day==4:
        meal = "VenerdiPRANZO"
        kw = "VP"
    elif day==5:
        meal = "VenerdiCENA"
        kw = "VC"

    ID = StringVar()                        #Make the ID entry as a string format
    tag = cless.connect(rdwr={'on-connect': lambda tag: False})     #Read the Unique ID (UID) of the NFC tag
    #beep = cless.connect(rdwr={'beep-on-connect':True})     #Enable beeping for near device communication
    ID = tag.identifier.encode("hex")                       #Convert UID to hex base
    cless.close()                           #Close NFC bus

    name.configure (text= "Braccialetto: %s" % (ID))
    name.update()

    print "Braccialetto: ", ID
    cursor = db.cursor()                    #Create MySQL DB pointer
    cursor.execute("SELECT Tipo FROM %s WHERE ID_Bracelet = '%s'" % (db_table, ID))  #Execute DB query to fetch meal type (Carnet or Single)
    result = cursor.fetchall()              #Fetch results into an array
    
    if machine == 1:                        #Bind machine ID to meal name
        portate = "Primo"
    if machine == 2:
        portate = "Secondo"
    if machine == 3:
        portate = "Dessert"

    if cursor.rowcount == 0:                #If bracelet UID is not found in MySQL DB, return an error message
        status.configure(text="BRACCIALETTO NON REGISTRATO", background="orange")  
        print ("Non registrato")
        status.update()
        sleep(0.3)
    for row in result:                      #If bracelet UID is foung, continue with device meal validation (in case it's a Carnet meal type)
        if "Carnet" in row[0]:
            cursor.execute ("SELECT %s FROM %s WHERE ID_Bracelet = '%s'" % (portate, db_table, ID))  #Select meal to check if it's already been taken by customer.
            validation = cursor.fetchall()
            if day in validation[0]:        #Check previously validations (as declared above)
                print("Already Used")
                status.configure (text="PIETANZA GIA" + u'\u0300' +" RISCATTATA", background = "orange")
                status.update()
                cursor.execute("SELECT Last_Use FROM %s WHERE ID_Bracelet = '%s'" % (db_table, ID))
                last = cursor.fetchall()
                last_use.configure(text = "Ultimo utilizzo: %s" % (last[0]))
                last_use.update()
                sleep(0.3)
            else:                           #if meal has not been taken before, validate the NFC tag checking if it's enabled to that specific meal.
                currentDT = datetime.datetime.now()     #Extract date and time from PC
                cursor.execute("UPDATE %s SET Last_Use = '%s' WHERE ID_BRACELET = '%s'" % (db_table, str(currentDT)[:19], ID))      #Insert date and time into MySQL db
                db.commit()
                print("Valid")
                status.configure (text="CARNET: VALID", background = "green")   #Display valid output
                status.update()
                cursor.execute("UPDATE %s SET %s=%s WHERE ID_BRACELET='%s'" % (db_table, portate, day, ID))  #Set meal counter to day ID to prevent the "taking-again"
                db.commit()
        else:
            cursor.execute ("SELECT %s FROM %s WHERE ID_Bracelet = '%s'" % (portate, db_table, ID))  #If coupon is not a "Carnet" type, proceed to single day validation
            validation = cursor.fetchall()
            if day in validation[0]:        #Check previously validations (as declared above)
                print("Already Used")
                status.configure (text="PIETANZA GIA" + u'\u0300' +" RISCATTATA", background = "orange")
                status.update()
                cursor.execute("SELECT Last_Use FROM %s WHERE ID_Bracelet = '%s'" % (db_table, ID))
                last = cursor.fetchall()
                last_use.configure(text = "Ultimo utilizzo: %s" % (last[0]))
                last_use.update()
                sleep(0.5)
            else:                           #if meal has not been taken before, validate the NFC tag checking if it's enabled to that specific meal.
                db.commit()
                cursor.execute("SELECT Pasti FROM %s WHERE ID_Bracelet = '%s'" % (db_table, ID))     #Select the single meal table, to check which meal are enabled
                results = cursor.fetchall()
                for rows in results:   
                    if kw in rows[0]:       #Check the fetched result, precisely if the present meal is enabled.
                        currentDT = datetime.datetime.now()     #Extract date and time from PC
                        cursor.execute("UPDATE %s SET Last_Use = '%s' WHERE ID_BRACELET = '%s'" % (db_table, str(currentDT)[:19], ID))      #Insert date and time into MySQL db
                        db.commit()
                        print ("Valid")     #Display valid output
                        status.configure (text="VALID", background = "green")
                        status.update()
                        cursor.execute("UPDATE %s SET %s=%s WHERE ID_BRACELET='%s'" % (db_table, portate, day, ID))  #Set meal counter to day ID to prevent the "taking-again"
                        db.commit()

                    else:
                        print ("Not Valid") #Display invalid output
                        status.configure (text="NOT VALID", background = "red")  
                        status.update()
    cursor.close()                          #Close DB pointer
    db.close()                              #Close DB connection
    clear_textbox()                         #Clear the verification module in order to be able to verify another customer
  

#=============================================================================

# --- GRAPHIC INTERFACE DEFINITION ---

app = Tk()
app.title("Tutto e" + u'\u0300' + " Numero - Food Convalidator")

app.geometry("900x850+500+70")

title = Label (app, text="Tutto e" + u'\u0300' +" Numero 2019", font=("Bahnschrift", 50), fg="#2077bf").pack(padx = 5, pady =0) #Title

row1 = Label(app, text = "Convalida Pasti", font=("Bahnschrift", 35), fg="#d34343").pack(padx = 20, pady = 0) #First text row


#the variable
bv = StringVar()
meal = StringVar()


#the entry box
b1 = Entry(app, textvariable=bv, font=("Bahnschrift", 44))
b1.pack(padx = 20, pady = 15)
b1.focus_force()

status = Label(app, text="IN ATTESA", font=("Bahnschrift", 35), background="#cedbef")
status.pack(padx = 20, pady = 30)

name = Label(app, text="Braccialetto: ", font=("Bahnschrift", 28))
name.pack(pady = 5)

#b1.bind("<Button-1>", validate)
b1.bind("<Return>", validate)


bu1 = Button(app, text="Convalida", font=("Bahnschrift", 30))
bu1.pack(padx = 20, pady = 20)
bu1.bind("<Button-1>", validate)
bu1.bind("<Return>", validate)

quitter = Button(app, text="Esci", font=("Bahnschrift", 30), command = quit)
quitter.pack(padx = 5, pady = 5)

if day== 1:
    meal = "Mercoledi CENA"
elif day==2:
    meal = "Giovedi PRANZO"
elif day==3:
    meal = "Giovedi CENA"
elif day==4:
    meal = "Venerdi PRANZO"
elif day==5:
    meal = "Venerdi CENA"

date = Label(text = "Pasto: %s" % (meal), font=("Bahnschrift", 20), background = "#99ffe0")
date.pack(pady = 25)

if machine==1:
    loc = "PRIMI PIATTI"
elif machine==2:
    loc = "SECONDI PIATTI"
elif machine==3:
    loc = "FRUTTA / DESSERT"

type = Label(text = "Convalida: %s" % (loc), font=("Bahnschrift", 20), background = "#ffbb00")
type.pack()

last_use = Label(text="Ultimo utilizzo: ", font=("Bahnschrift", 20))
last_use.pack(pady=20)


def quit():
    app.destroy()

def clear_textbox():
    sleep(0.7)
    status.configure(text="IN ATTESA", background="#cedbef")
    b1.delete(0, END)
    bu1.configure (text="Convalida")
    bu1.update
    name.configure(text="Braccialetto:")
    name.update()
    last_use.configure(text="Ultimo utilizzo: ")
    last_use.update()

app.mainloop()