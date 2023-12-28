import queue 
import requests 
import sys 
import threading 

AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0" 
EXTENSIONS = ['.php', '.bak', '.orig', '.inc'] 
TARGET = "https://pentest85.wordpress.com/" 
THREADS = 50 
WORDLIST = "all.txt" 
OUTPUT_FILE = "activity.txt"  # File to save the activity

def get_words(resume=None):
    def extend_words(word):
        if "." in word: 
            words.put(f'/{word}') 
        else: 
            words.put(f'/{word}/')
        for extension in EXTENSIONS: 
            words.put(f'/{word}{extension}') 
    
    with open(WORDLIST) as f: 
        raw_words = f.read()
    
    found_resume = False 
    words = queue.Queue() 
    
    for word in raw_words.split(): 
        if resume is not None:
            if found_resume: 
                extend_words(word) 
            elif word == resume: 
                found_resume = True 
                print(f'Odczytywanie listy słów od: {resume}') 
        else: 
            print(word) 
            extend_words(word) 
    
    return words 

def dir_bruter(words): 
    headers = {'User-Agent': AGENT}
    output = []  # To store the activity to be written to the file
    while not words.empty(): 
        url = f'{TARGET}{words.get()}'
        try: 
            r = requests.get(url, headers=headers) 
        except requests.exceptions.ConnectionError:
            output.append(f'Failed to connect: {url}') 
            continue 
        
        if r.status_code == 200: 
            output.append(f'Success ({r.status_code}): {url}')
            print(f'Success ({r.status_code}): {url}')
        elif r.status_code == 404: 
            pass  # Do nothing for 404 status
        else: 
            output.append(f'{r.status_code} => {url}') 
            print(f'{r.status_code} => {url}')
    
    # Write the collected output to the file
    with open(OUTPUT_FILE, 'w') as file:
        file.write('\n'.join(output))

if __name__ == '__main__': 
    words = get_words()
    print('Press Enter to continue') 
    sys.stdin.readline() 
    
    for _ in range(THREADS): 
        t = threading.Thread(target=dir_bruter, args=(words,))
        t.start()
