from pypdf import PdfReader, DocumentInformation

def printMetaData(fileName: str) -> None:
    """
    Opens a PDF file and prints its metadata
    
    :param fileName: PDF filename
    :type str
    """
    try:
        with open(fileName, "rb") as pdfFile:
            reader: PdfReader = PdfReader(pdfFile)
        
            metaData: DocumentInformation|None = reader.metadata
        
            print(f"\n [*] PDF MetaData for: {fileName}")
            for metaItem in metaData:
                print(f"[+] {metaItem}: {metaData[metaItem]}")
    except Exception as e:
        print(f"[-] Error reading {fileName}: {e}")

def main() -> None:
    printMetaData(fileName="test.pdf")

if __name__ == "__main__":
    main()