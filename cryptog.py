import os, random
import Tkinter, tkFileDialog
import getpass
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def encrypt(key, filename):
    chunksize = 64*1024
    outputFile = "Crypted"+filename
    fileSize = str(os.path.getsize(filename)).zfill(16)
    IV = ''

    for i in range(16):
        IV += chr(random.randint(0, 0xFF))

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(fileSize)
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))
                os.remove(filename)

def decrypt(key, filename):
        chunksize = 64*1024
        outputFile = filename[7:]

        with open(filename, 'rb') as infile:
                filesize = long(infile.read(16))
                IV = infile.read(16)

                decryptor = AES.new(key, AES.MODE_CBC, IV)

                with open(outputFile, 'wb') as outfile:
                        while True:
                                chunk = infile.read(chunksize)

                                if len(chunk) == 0:
                                        break

                                outfile.write(decryptor.decrypt(chunk))
                                os.remove(filename)
                        outfile.truncate(filesize)

def getKey(password):
    hasher = SHA256.new(password)
    return hasher.digest()

def Main():

    option = raw_input("\n O que deseja fazer a seguir? \n (E) Encriptar \n (D)Decriptar \n (0) Sair \n")
    while(option != '0'):
            if option == 'E' or option == 'e':
                print("Escolha o arquivo para ser criptografado")
                try:
                    root = Tkinter.Tk()
                    root.withdraw()

                    file_path = tkFileDialog.askopenfilename()
                    value = os.path.basename(file_path)
                    if ('encrypted' in value):
                        print "\nOps!\nEsse arquivo ja esta criptografado"
                        Main()
                    else:
                        filename = value
                        password = getpass.getpass("Senha: ")
                        encrypt(getKey(password), filename)
                        print("Done!")
                        Main()
                except AttributeError:
                    print "\nNada foi selecionado!"
                    Main()
            elif option == 'D' or option == 'd':
                print("Escolha o arquivo para ser decriptografado")
                try:
                    root = Tkinter.Tk()
                    root.withdraw()

                    file_path = tkFileDialog.askopenfilename()
                    value = os.path.basename(file_path)
                    if not ('encrypted' in value):
                        print "\nOps!\nEsse arquivo nao esta criptografado"
                        Main()
                    else:
                        filename = value
                        password = getpass.getpass("Senha: ")
                        decrypt(getKey(password), filename)
                        print("Done!")
                        Main()
                except AttributeError:
                    print "\nNada foi selecionado!"
                    Main()
            else:
                option = raw_input("O que deseja fazer a seguir? \n (1) Encriptar \n (2)Decriptar \n (0) Sair\n")
    print "Finalizado!"
    quit()
if __name__ == '__main__':
    Main()
