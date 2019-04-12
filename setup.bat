@echo off

echo Benvenuto nel programma di configurazione del sistema di validazione elettronica di "Tutto e' Numero"!

echo 1)Inserire l'indirizzo IP del server nel file "address.txt"

echo 2)Premere un tasto per avviare la configurazione
pause
@echo on
echo
xcopy /y %appdata%\LPDEV\Tutto_e_numero_19\NFC\address.txt %appdata%\LPDEV\Tutto_e_numero_19\NFC\Check-In\Offline
xcopy /y %appdata%\LPDEV\Tutto_e_numero_19\NFC\address.txt %appdata%\LPDEV\Tutto_e_numero_19\NFC\Check-In\Online
xcopy /y %appdata%\LPDEV\Tutto_e_numero_19\NFC\address.txt %appdata%\LPDEV\Tutto_e_numero_19\NFC\Check-out
xcopy /y %appdata%\LPDEV\Tutto_e_numero_19\NFC\address.txt %appdata%\LPDEV\Tutto_e_numero_19\NFC\Validazione
pause
