from crypto import encriptar_variable

passw = str(input ('Ingrese pass : '))
passw1 = bytes(passw.encode('utf-8'))
pass_encript = encriptar_variable(passw1)
print (passw1)
print (pass_encript)