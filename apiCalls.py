from fileIO import getConfig
from media import Book
import requests

conf = getConfig()
apiKey = conf['API_KEY']
apiUrl = str(conf['API_URL']).replace("{{KEY}}", apiKey)

def getBook(isbn):
    bk = Book("isbn is not in the db")
    print(bk._test)
    return requests.get(apiUrl + isbn).text
