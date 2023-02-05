import requests_cache
from bs4 import BeautifulSoup
import os
from datetime import timedelta, datetime

session = requests_cache.CachedSession(".cache", expire_after=timedelta(hours=24))

try:
    os.mkdir("data/")
except FileExistsError:
    pass

print("Tento program je rozšiřován v naději, že bude užitečný, avšak BEZ JAKÉKOLIV ZÁRUKY. Neposkytují se ani odvozené záruky PRODEJNOSTI anebo VHODNOSTI PRO URČITÝ ÚČEL. Další podrobnosti hledejte v Obecné veřejné licenci GNU.")

def downloadPDF(link, path, title):
    r = session.get(f"http://www.realisticky.cz/{link}")
    with open(f"{path}/{title}.pdf", 'wb') as f:
        f.write(r.content)

def createStructure(bread):
    paths = ["data"]
    for i in range(len(bread)):
        path = os.path.join(paths[-1],bread[i])
        paths.append(path)
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
    return paths[-1]


hodina = 1
while True:
    r = session.get(f"http://www.realisticky.cz/hodina.php?id={hodina}")
    r.encoding = r.apparent_encoding
    
    soup = BeautifulSoup(r.text, features="html.parser")
    
    bread = soup.find("small").text.replace("\n","").split("»")
    bread = [i.strip() for i in bread if len(i) > 1]
    final = createStructure(bread)

    title = soup.find("h2").text
    print(f"Scraping '{title}'")

    lekce = soup.find("a", target="_blank")
    if lekce is None:
        print(f"Done! Scraped {hodina} pages!")
        quit(0)
    downloadPDF(lekce["href"], final, title)
    
    priklady = soup.find_next("a", target="_blank")
    downloadPDF(lekce["href"], final, title+" příklady")
    
    print(f"Scraped '{title}'")
    hodina += 1
