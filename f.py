import requests

url = 'http://127.0.0.1:8000/accounts/login/manager/'

session = requests.Session()
resp0 = session.get(url)

print(resp0.text)  # This will print the HTML content of the page

