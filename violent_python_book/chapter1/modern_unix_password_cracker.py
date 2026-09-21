import crypt

DICT_FILENAME: str = "dictionary.txt"
PASSWORD_FILENAME: str = "passwords.txt"

def testPass(cryptPass) -> None:
    salt_prefix: str = cryptPass[0:11]
    
    dictFile = open(DICT_FILENAME, "r")
    
    for word in dictFile.readlines():
        word = word.strip("\n")
        
        cryptWord: str = crypt.crypt(word, salt_prefix)
        
        if (cryptPass == cryptWord):
            print("[+] Found Password:" + word + "\n")
            dictFile.close()
            return
    print("[-] Password Not Found.\n")
    return

def main():
    passFile = open(PASSWORD_FILENAME, "r")
    
    for line in passFile.readlines():
        user: str = line.split(":")[0]
        cryptPass: str = line.split(":")[1].strip(" ")
        
        print("[*] Cracking Password For: " + user)
        testPass(cryptPass)
    passFile.close()

if __name__ == "__main__":
    main()