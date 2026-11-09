import bs4
from pathlib import Path
from requests import Response, get
from PIL import Image
from PIL.ExifTags import TAGS

def requestHtml(url: str) -> str:
    """
    Gets the url and returns the response as string
    
    :param url: Target url
    :type str
    
    :return: Response content as text
    :rtype: str
    """
    response: Response = get(url=url)
    return response.text

def findImages(sourceCode: str) -> list:
    """
    Reads the source code and identifies all image tags
    
    :param sourceCode: Source code
    :type str
    
    :return: Image Tags
    :rtype: list
    """
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(sourceCode)
    imgTags: list = soup.find_all("img")
    return imgTags

def printImage(url: str, imgTag) -> str:
    """
    Downloads the image and if successful response writes the image bytes to the file system
    
    :param url: Root url
    :type str
    
    :param imgTag: Image tags
    
    :return: Image file name on success, empty string on error
    :rtype: str
    """
    try:
        imgSrc: str = imgTag["src"]
        print(f"[*] Downloading image: {imgSrc}")
        imgResponse: Response = get(url=imgSrc)
        if imgResponse.status_code == 200:
            imgContent: bytes = imgResponse.content
        else:
            raise
        imgSrcPath: Path = Path(imgSrc)
        imgFileName: str = imgSrcPath.name
        
        with open(imgFileName, "wb") as imgFile:
            imgFile.write(imgContent)
        return imgFileName
    except Exception as e:
        print(e)
        return ""

def testForExif(imgFileName: str) -> None:
    try:
        exifData: dict = {}
        imgFile= Image.open(imgFileName)
        info = imgFile.getexif()
        if info:
            for k,v in info.items():
                decoded = TAGS.get(k, k)
                exifData[decoded] = v
            exifGPS = exifData["GPSInfo"]
            if exifGPS:
                print(f"[*] {imgFileName} contains GPS MetaData")
            else:
                print(f"[-] No GPS data for {imgFileName}")
        else:
            print(f"[-] No exif info for {imgFileName}")
    except Exception as e:
        print(e)

def main() -> None:
    url: str = ""
    response: str = requestHtml(url=url)
    imageTags: list = findImages(sourceCode=response)
    for imgTag in imageTags:
        imgFileName: str = printImage(url=url, imgTag=imgTag)
        testForExif(imgFileName=imgFileName)

if __name__ == "__main__":
    main()


