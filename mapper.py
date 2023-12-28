# from io import BytesIO 
# from lxml import etree 
# import requests 
# url = 'https://pentest85.wordpress.com'
# r = requests.get(url) # GET ❷
# content = r.content # Treść jest typu bajtowego
# parser = etree.HTMLParser() 
# content = etree.parse(BytesIO(content), parser=parser) # Przekształcenie w drzewo ❸
# for link in content.findall('//a'): # Wyszukanie wszystkich znaczników "a" ❹
#  print(f"{link.get('href')} -> {link.text}") 
##############################################3
import contextlib 
import os 
import queue 
import requests 
import sys 
import threading 
import time 
FILTERS = [".jpg", ".gif", ".png", ".css"] 
TARGET = "https://pentest85.wordpress.com"
THREADS = 10 
answers = queue.Queue() 
web_paths = queue.Queue() 
def gather_paths(): 
    for root, _, files in os.walk('.'):
        for fname in files: 
            if os.path.splitext(fname)[1] in FILTERS: 
                continue 
            path = os.path.join(root, fname) 
            if path.startswith('.'): 
                path = path[1:] 
            print(path) 
            web_paths.put(path) 
@contextlib.contextmanager 
def chdir(path):
    """ 
    Na początku następuje przejście do wskazanego katalogu. 
    Na koniec następuje powrót do pierwotnego katalogu. 
    """ 
    this_dir = os.getcwd() 
    os.chdir(path) 
    try: 
        yield
    finally: 
        os.chdir(this_dir)

def test_remote(): 
    while not web_paths.empty():
        path = web_paths.get()
        url = f'{TARGET}{path}' 
        time.sleep(2) # Docelowy serwer może dławić żądania ❸
        r = requests.get(url) 
        if r.status_code == 200: 
            answers.put(url) 
            sys.stdout.write('+') 
        else: 
            sys.stdout.write('x') 
        sys.stdout.flush() 

def run(): 
    mythreads = list() 
    for i in range(THREADS):
        print(f'Uruchomienie wątku {i}') 
        t = threading.Thread(target=test_remote) 

        mythreads.append(t) 
        t.start() 
    for thread in mythreads: 
        thread.join()

if __name__ == '__main__': 
    with chdir("/workspaces/BHPython/wordpress"):
        gather_paths() 
    input('Naciśnij Enter, aby kontynuować')
    run()
    with open('myanswers.txt', 'w') as f:
        while not answers.empty(): 
            f.write(f'{answers.get()}\n') 
    print('Koniec')


############################################################
# import contextlib
# import os
# import queue
# import requests
# import sys
# import threading
# import time

# FILTERS = [".jpg", ".gif", ".png", ".css"]
# TARGET = "https://pentest85.wordpress.com"
# THREADS = 10

# answers = queue.Queue()
# web_paths = queue.Queue()

# def gather_paths():
#     for root, _, files in os.walk('.'):
#         for fname in files:
#             if os.path.splitext(fname)[1] in FILTERS:
#                 continue
#             path = os.path.join(root, fname)
#             if path.startswith('.'):
#                 path = path[1:]
#             print(path)
#             web_paths.put(path)

# @contextlib.contextmanager
# def chdir(path):
#     """
#     On enter, change directory to specified path.
#     On exit, change directory to original.
#     """
#     this_dir = os.getcwd()
#     os.chdir(path)
#     try:
#         yield
#     finally:
#         os.chdir(this_dir)

# def test_remote():
#     while not web_paths.empty():
#         path = web_paths.get()
#         url = f'{TARGET}{path}'
#         time.sleep(2)
#         r = requests.get(url)
#         if r.status_code == 200:
#             answers.put(url)
#             sys.stdout.write('+')
#         else:
#             sys.stdout.write('x')
#         sys.stdout.flush()

# def run():
#     mythreads = list()
#     for i in range(THREADS):
#         print(f'Spawning thread {i}')
#         t = threading.Thread(target=test_remote)
#         mythreads.append(t)
#         t.start()

#     for thread in mythreads:
#         thread.join()

# if __name__ == '__main__':
#     with chdir("C:\\Users\\Damwid\\Downloads\\wordpress-6.4.2\\wordpress"):
#         gather_paths()
#     input('Press ENTER to continue...')
#     run()
#     with open('myanswers.txt', 'w') as f:
#         while not answers.empty():
#             f.write(f'{answers.get()}\n')
#     print('done')




    ############################################
