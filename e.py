from io import BytesIO 
from lxml import etree 
import requests 
url = 'https://pentest85.wordpress.com'
r = requests.get(url) # GET ❷
content = r.content # Treść jest typu bajtowego
parser = etree.HTMLParser() 
content = etree.parse(BytesIO(content), parser=parser) # Przekształcenie w drzewo ❸
for link in content.findall('//a'): # Wyszukanie wszystkich znaczników "a" ❹
 print(f"{link.get('href')} -> {link.text}") 