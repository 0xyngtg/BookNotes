import argparse
import pyzipper
from threading import Thread

#ZIP_FILE : ZipFile = ZipFile("chapter1.zip")
#PASS_FILE = "dictionary.txt"

def defineArguments() -> argparse.Namespace:
    """"""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Performs dictionary attack against the specified zip file."
    )
    parser.add_argument("-w", "--wordlist", required=True)
    parser.add_argument("-z", "--zip", required= True)
    return parser.parse_args()

def extractFile(zFilePath: str, password: str) -> None:
    """"""
    try:
        with pyzipper.AESZipFile(zFilePath) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                zf.read(name=info.filename, pwd=password.encode())
            print("Password found:", password)
    except RuntimeError:
        pass
    except Exception as e:
        print(f"Unhandled error: {e}")

def main() -> None:
    """"""
    args: argparse.Namespace = defineArguments()
    
    with open(args.wordlist, "r") as f:
        for password in f.readlines():
            th: Thread = Thread(target=extractFile, args=[args.zip, password.rstrip()])
            th.start()

if __name__ == "__main__":
    main()
